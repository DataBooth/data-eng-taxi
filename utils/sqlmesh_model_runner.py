from pathlib import Path
import duckdb
import sqlglot
from loguru import logger
import re
from collections import defaultdict, deque


class SQLMeshModelRunner:
    def __init__(self, database):
        logger.info("Initializing DuckDB instance.")
        if database:
            self.con = duckdb.connect(database)
        else:
            self.con = duckdb.connect(database=":memory:")

    def _parse_model_name(self, sql_file_path):
        sql_path = Path(sql_file_path)
        content = sql_path.read_text(encoding="utf-8")
        match = re.search(
            r"MODEL\s*\(\s*name\s+([a-zA-Z0-9_.]+)", content, re.IGNORECASE
        )
        if match:
            model_name = match.group(1)
            logger.debug(f"Found model name: {model_name}")
            return model_name
        logger.warning(f"No model name found in {sql_file_path}")
        return None

    def _extract_pure_sql(self, sql_file_path):
        sql_path = Path(sql_file_path)
        lines = sql_path.read_text(encoding="utf-8").splitlines()
        pure_sql_lines = []
        in_directive = False

        for line in lines:
            stripped = line.strip()
            if stripped.upper().startswith(("MODEL", "AUDIT", "MACRO")):
                in_directive = True
                continue
            if in_directive and re.match(r"^\)\s*;?\s*$", stripped):
                in_directive = False
                continue
            if in_directive or stripped.upper().startswith(("MODEL", "AUDIT", "MACRO")):
                continue
            if not stripped or stripped.startswith("--"):
                continue
            pure_sql_lines.append(line)
        pure_sql = "\n".join(pure_sql_lines).strip()
        logger.debug("Extracted SQL (after removing directives):\n{}", pure_sql)
        return pure_sql

    def _find_dependencies(self, sql, all_model_names):
        # Find all words in the SQL that match model names (simple heuristic)
        deps = []
        for name in all_model_names:
            # Match as whole word, possibly schema-qualified
            pattern = re.compile(rf"\b{name}\b", re.IGNORECASE)
            if pattern.search(sql):
                deps.append(name)
        logger.debug(f"Dependencies found: {deps}")
        return deps

    def _show_dependencies(self, model_file_paths):
        """
        Print the dependency mapping for the given model files.
        """
        # Parse all model names first
        model_names = {self._parse_model_name(p): p for p in model_file_paths}
        dependencies = defaultdict(list)
        for name, path in model_names.items():
            sql = self._extract_pure_sql(path)
            deps = self._find_dependencies(sql, model_names.keys() - {name})
            dependencies[name].extend(deps)
        logger.info("Model dependency mapping:")
        for model, deps in dependencies.items():
            logger.info(f"  {model}: {deps if deps else 'No dependencies'}")
        return dependencies

    def transpile_sql(self, sql, target_dialect="duckdb", source_dialect="duckdb"):
        logger.debug(f"Transpiling SQL from {source_dialect} to {target_dialect}.")
        try:
            transpiled = sqlglot.transpile(
                sql, read=source_dialect, write=target_dialect
            )[0]
            logger.debug("Transpiled SQL:\n{}", transpiled)
            return transpiled
        except Exception as e:
            logger.error(f"SQLGlot failed to parse/transpile: {e}")
            return sql

    def execute_sqlmesh_model(
        self,
        sql_file_path,
        params=None,
        target_dialect="duckdb",
        source_dialect="duckdb",
        materialize_as="view",
    ):
        model_name = self._parse_model_name(sql_file_path)
        sql = self._extract_pure_sql(sql_file_path)
        if not sql:
            logger.warning(f"No SQL found in {sql_file_path}. Nothing to execute.")
            return
        if params:
            sql = sql.format(**params)
        transpiled_sql = self.transpile_sql(
            sql, target_dialect=target_dialect, source_dialect=source_dialect
        )
        if model_name:
            if "." in model_name:
                schema = model_name.split(".")[0]
                create_schema_stmt = f"CREATE SCHEMA IF NOT EXISTS {schema};"
                logger.debug(f"Ensuring schema exists: {schema}")
                self.con.execute(create_schema_stmt)
            if materialize_as == "table":
                create_stmt = (
                    f"CREATE OR REPLACE TABLE {model_name} AS {transpiled_sql}"
                )
            else:
                create_stmt = f"CREATE OR REPLACE VIEW {model_name} AS {transpiled_sql}"
            logger.info(
                f"Materializing model as a {materialize_as.upper()}: {model_name}"
            )
            logger.debug("Executing:\n{}", create_stmt)
            self.con.execute(create_stmt)

    def execute_models_with_dependencies(self, model_file_paths, materialize_as="view"):
        # Parse all model names first
        model_names = {self._parse_model_name(p): p for p in model_file_paths}
        # Parse all dependencies
        dependencies = defaultdict(list)
        sqls = {}
        for name, path in model_names.items():
            sql = self._extract_pure_sql(path)
            sqls[name] = sql
            deps = self._find_dependencies(sql, model_names.keys() - {name})
            dependencies[name].extend(deps)
        # Topological sort
        order = list(reversed(self._topological_sort(dependencies)))

        logger.info(f"Model build order: {order}")
        for name in order:
            self.execute_sqlmesh_model(model_names[name], materialize_as=materialize_as)

    def _topological_sort(self, dependencies):
        # Kahn's algorithm
        in_degree = {k: 0 for k in dependencies}
        for deps in dependencies.values():
            for dep in deps:
                in_degree[dep] += 1
        queue = deque([k for k, v in in_degree.items() if v == 0])
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for dep in dependencies[node]:
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)
        if len(order) != len(dependencies):
            raise Exception("Circular dependency detected!")
        return order

    def query(self, sql, params=None):
        logger.info("Running query:\n{}", sql)
        if params:
            sql = sql.format(**params)
        return self.con.execute(sql).fetchall()

    def query_df(self, sql, params=None):
        logger.info("Running query (returning DataFrame):\n{}", sql)
        if params:
            sql = sql.format(**params)
        return self.con.execute(sql).df()

    def close(self):
        logger.info("Closing DuckDB connection.")
        self.con.close()


# Example usage:
if __name__ == "__main__":
    runner = SQLMeshModelRunner("yellow_taxi.duckdb")
    model_files = [
        "models/yellow_tripdata_seed.sql",
        "models/yellow_tripdata_cleaned.sql",
        "models/yellow_tripdata_daily_agg.sql",
        # Add more model files in your dependency chain here
    ]
    runner._show_dependencies(model_files)
    runner.execute_models_with_dependencies(model_files)
    results = runner.query("SELECT COUNT(*) FROM nyc.yellow_tripdata_seed")
    logger.info(f"Query datasize results: {results[0][0]}")

    # Transpile the model's SQL to databricks for inspection
    pure_sql = runner._extract_pure_sql("models/yellow_tripdata_seed.sql")
    databricks_sql = runner.transpile_sql(
        pure_sql, target_dialect="databricks", source_dialect="duckdb"
    )
    print()
    print("Original (DuckDB) SQL:\n")
    print(pure_sql)
    print("-" * 60)
    print("Databricks SQL:")
    print(databricks_sql)
    runner.close()
