from prefect import flow, task
import subprocess


@task
def run_sqlmesh(gateway="duckdb"):
    subprocess.run(
        ["sqlmesh", "plan", "--gateway", gateway, "--auto-apply"], check=True
    )
    subprocess.run(["sqlmesh", "run", "--gateway", gateway], check=True)


@flow(log_prints=True)
def run_taxi_pipeline(gateway="duckdb"):
    run_sqlmesh(gateway)


# if __name__ == "__main__":
#     run_taxi_pipeline.serve(
#         name="taxi-pipeline-deployment",
#         cron="0 2 * * *",  # Run daily at 2am
#         tags=["nyc-taxi", "sqlmesh"],
#         description="Runs the NYC Taxi data pipeline using SQLMesh.",
#     )
