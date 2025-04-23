-- models/yellow_tripdata_cleaned.sql
MODEL (
  name nyc.yellow_tripdata_cleaned,
  kind FULL
);

SELECT
  *
FROM
  nyc.yellow_tripdata
WHERE
  passenger_count IS NOT NULL
  AND trip_distance > 0
  AND fare_amount > 0
  AND tpep_pickup_datetime IS NOT NULL
  AND tpep_dropoff_datetime IS NOT NULL
;
