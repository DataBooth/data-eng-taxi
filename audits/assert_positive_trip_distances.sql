AUDIT assert_positive_trip_distances;

ASSERT SELECT COUNT(*) = 0 FROM {target} WHERE trip_distance < 0;
