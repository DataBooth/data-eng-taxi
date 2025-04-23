-- models/yellow_tripdata_daily_agg.sql
MODEL (
  name nyc.yellow_tripdata_daily_agg,
  kind INCREMENTAL_BY_TIME_RANGE,
  time_column 'tpep_pickup_datetime'
);

SELECT
  DATE(tpep_pickup_datetime) AS trip_date,
  COUNT(*) AS num_trips,
  SUM(fare_amount) AS total_fare
FROM
  nyc.yellow_tripdata_cleaned
GROUP BY
  trip_date
;
