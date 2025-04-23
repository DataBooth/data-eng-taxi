# data-eng-taxi

Data Engineering example using NYC taxi data (with SQLMesh, DuckDB, Databricks and Prefect)


# NYC Taxi Pipeline

## Overview

This repository demonstrates a robust, production-ready data engineering pipeline using [**SQLMesh**](https://sqlmesh.com), with [**DuckDB**](https://duckdb.org) for local development and [**Databricks**](https://databricks.com) for scalable cloud execution. 

The pipeline ingests, transforms, and summarises a full year of NYC Yellow Taxi trip data (20GB+), illustrating better practices in data modeling, testing, and cross-environment portability using robust open-source tooling.

---

## Table of Contents

- [data-eng-taxi](#data-eng-taxi)
- [NYC Taxi Pipeline](#nyc-taxi-pipeline)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Project Goals](#project-goals)
  - [Architecture and Tools](#architecture-and-tools)
  - [How It Works](#how-it-works)
  - [Why This Approach?](#why-this-approach)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Testing \& Validation](#testing--validation)
  - [Extending the Project](#extending-the-project)
  - [Contact](#contact)

---

## Project Goals

- **Showcase end-to-end data engineering skills**: from ingestion to transformation, orchestration, and testing.
- **Demonstrate SQLMesh’s power**: for environment management, versioning, and SQL dialect portability.
- **Enable seamless local-to-cloud development**: prototype on DuckDB, scale on Databricks.
- **Promote reproducibility and robust testing**: using real-world, large-scale open data.
- **Robust automation and observability**: employing Prefect.

---

## Architecture and Tools

| Component | Purpose | Why Chosen? |
| :-- | :-- | :-- |
| **SQLMesh** | Data pipeline management \& orchestration | Modern, versioned, cross-SQL support |
| **DuckDB** | Local dev \& fast prototyping | Lightweight, fast, SQL-compliant |
| **Databricks** | Scalable cloud execution | Handles large data, industry standard |
| **Prefect** | Automated execution | Handles large data, industry standard |
| **NYC TLC Data** | Realistic, open, large dataset | Public, well-known, >20GB/year |


---

## How It Works

1. **Data Ingestion**:
    - Downloads 12 months of NYC Yellow Taxi trip CSVs (~2GB each).
    - Data is staged in the `seeds/` directory.
  
2. **SQLMesh Models**:
    - **Seed Model**: Reads and unions all CSV files into a single logical table.
    - **Transformation Model**: Aggregates and summarises trip data (e.g., average total amount by passenger count).

3. **Environment Management**:
    - **DuckDB Gateway**: For local, rapid iteration.
    - **Databricks Gateway**: For production-scale processing.

4. **Testing**:
    - Unit tests on sample data ensure correctness and portability.
    - Aggregate statistics compared across engines for full-data validation.

5. **Orchestration**:
    - `sqlmesh plan` and `sqlmesh run` manage deployment and execution.
    - Easily switch between local and cloud with a config change.

---

## Why This Approach?

- **Portability**:
SQLMesh (via SQLGlot) allows you to write SQL models once and run them on any backend—no more rewriting for each engine.
- **Scalability**:
DuckDB is perfect for fast local dev; Databricks handles massive datasets in production.
- **Reproducibility \& Testing**:
Built-in testing and environment isolation reduce errors and make CI/CD feasible.
- **Real-World Relevance**:
Using a full year of NYC Taxi data ensures this is not a toy example. The pipeline is designed for real data engineering challenges: volume, schema evolution, and cross-engine consistency.

---

## Getting Started

### Prerequisites

- Python 3.8+
- [SQLMesh](https://sqlmesh.com/) (`uv add "sqlmesh[databricks,web]"` or `pip install sqlmesh`)
- [DuckDB](https://duckdb.org/) (installed automatically by SQLMesh)
- Databricks account (for cloud runs)
- [Prefect](https://prefect.io)


### Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/data-eng-taxi.git
cd data-eng-taxi
```

2. **Download the data:**
Download all 12 monthly parquet files from [NYC TLC](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
Place them in the `seeds/` directory.

e.g. [text](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet)

3. **Configure SQLMesh:**
    - For local runs, use the provided DuckDB config.
    - For Databricks, edit `config.yaml` with your workspace details.
4. **Run the pipeline:**

```bash
sqlmesh plan --gateway duckdb --auto-apply
sqlmesh run --gateway duckdb
# For Databricks:
sqlmesh plan --gateway databricks --auto-apply
sqlmesh run --gateway databricks
```


---

## Testing \& Validation

- **Unit Tests:**
Located in `tests/`. Run with:

```bash
sqlmesh test --gateway duckdb
sqlmesh test --gateway databricks
```

- **Data Consistency:**
Compare aggregate stats (e.g., row counts, sums) between environments to ensure correctness.

---

## Extending the Project

- Add more models (e.g., revenue by hour, trip distance analysis).
- Integrate with orchestration tools (e.g., Prefect, Airflow).
- Add CI/CD for automated testing and deployment.
- Explore incremental models for efficient updates.

---

## Contact

Questions?

Open an issue or reach out via [LinkedIn](https://www.linkedin.com/in/mjboothaus).

---

**This repository is designed to illustrate not just technical proficiency, but also a thoughtful, scalable approach to modern data engineering.**


