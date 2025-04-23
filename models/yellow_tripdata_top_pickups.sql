-- models/yellow_tripdata_top_pickups.sql
MODEL (
  name nyc.yellow_tripdata_top_pickups,
  kind FULL
);

SELECT
  PULocationID,
  COUNT(*) AS trip_count
FROM
  nyc.yellow_tripdata_cleaned
GROUP BY
  PULocationID
ORDER BY
  trip_count DESC
LIMIT 10
;
