# NYC Yellow Taxi Trip Records Data Dictionary

_Last updated: March 18, 2025_

This document describes the schema and fields for the NYC Yellow Taxi Trip Records dataset. For additional data dictionaries (e.g., for other trip types) and metadata such as TLC Taxi Zones, see the [NYC TLC Trip Record Data page](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml).

---

## Table of Contents

- [NYC Yellow Taxi Trip Records Data Dictionary](#nyc-yellow-taxi-trip-records-data-dictionary)
  - [Table of Contents](#table-of-contents)
  - [Field Descriptions](#field-descriptions)
  - [Reference Links](#reference-links)
  - [References](#references)

---

## Field Descriptions

| Field Name | Description | Values / Codes |
| :-- | :-- | :-- |
| **VendorID** | Code indicating the TPEP provider that provided the record. | 1 = Creative Mobile Technologies, LLC<br>2 = Curb Mobility, LLC<br>6 = Myle Technologies Inc<br>7 = Helix |
| **tpep_pickup_datetime** | The date and time when the meter was engaged (trip started). | Datetime (e.g., `2025-01-01 13:45:30`) |
| **tpep_dropoff_datetime** | The date and time when the meter was disengaged (trip ended). | Datetime |
| **passenger_count** | Number of passengers in the vehicle. | Integer |
| **trip_distance** | Elapsed trip distance in miles reported by the taximeter. | Float (miles) |
| **RatecodeID** | Final rate code in effect at end of trip. | 1 = Standard<br>2 = JFK<br>3 = Newark<br>4 = Nassau/Westchester<br>5 = Negotiated fare<br>6 = Group ride<br>99 = Null/unknown |
| **store_and_fwd_flag** | Was the trip record held in vehicle memory before sending to the vendor? | Y = store and forward<br>N = not a store and forward trip |
| **PULocationID** | TLC Taxi Zone where the meter was engaged (pickup). | Integer (see TLC Taxi Zones) |
| **DOLocationID** | TLC Taxi Zone where the meter was disengaged (dropoff). | Integer (see TLC Taxi Zones) |
| **payment_type** | How the passenger paid for the trip. | 0 = Flex Fare<br>1 = Credit card<br>2 = Cash<br>3 = No charge<br>4 = Dispute<br>5 = Unknown<br>6 = Voided trip |
| **fare_amount** | Time-and-distance fare calculated by the meter. | Float (USD) |
| **extra** | Miscellaneous extras and surcharges. | Float (USD) |
| **mta_tax** | Tax automatically triggered based on the metered rate in use. | Float (USD) |
| **tip_amount** | Tip amount (automatically populated for credit card tips; cash tips not included). | Float (USD) |
| **tolls_amount** | Total amount of all tolls paid in trip. | Float (USD) |
| **improvement_surcharge** | Improvement surcharge assessed at the flag drop (levied since 2015). | Float (USD) |
| **total_amount** | Total amount charged to passengers (does not include cash tips). | Float (USD) |
| **congestion_surcharge** | Total amount collected in trip for NYS congestion surcharge. | Float (USD) |
| **airport_fee** | Fee for pickups only at LaGuardia and JFK airports. | Float (USD) |
| **cbd_congestion_fee** | Per-trip charge for MTA's Congestion Relief Zone (starting Jan. 5, 2025). | Float (USD) |


---

## Reference Links

- [NYC TLC Yellow Taxi Trip Data Dictionary (PDF)](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
- [TLC Taxi Fare Information](https://www.nyc.gov/site/tlc/passengers/taxi-fare.page)
- [TLC Trip Record Data Main Page](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml)

---

**Note:**

- For TLC Taxi Zone IDs (`PULocationID`, `DOLocationID`), refer to the official Taxi Zone lookup tables.
- For more details on fare calculation and surcharges, see the [TLC Taxi Fare Information](https://www.nyc.gov/site/tlc/passengers/taxi-fare.page).

---

*This README was generated on 23 April 2025, based on the official data dictionary as of March 18, 2025.*

## References

[^1]: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf