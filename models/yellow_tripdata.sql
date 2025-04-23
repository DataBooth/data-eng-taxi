MODEL (
name nyc.yellow_tripdata,
kind SEED
) ;

SELECT * FROM read_parquet('seeds/yellow_tripdata_202[3-5]-*.parquet') ;


-- MODEL (
--   name sqlmesh_example.seed_model,
--   kind SEED (
--     path '../seeds/seed_data.csv'
--   ),
--   columns (
--     id INTEGER,
--     item_id INTEGER,
--     event_date DATE
--   ),
--   grain (id, event_date)
-- );
  