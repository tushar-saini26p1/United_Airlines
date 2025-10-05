import duckdb
import pandas as pd

con = duckdb.connect(database=':memory:', read_only=False)

con.execute("CREATE OR REPLACE VIEW flight_level_data AS SELECT * FROM read_csv_auto('Flight Level Data.csv', sep='\t', header=True)")
con.execute("CREATE OR REPLACE VIEW pnr_flight_level_data AS SELECT * FROM read_csv_auto('PNR+Flight+Level+Data.csv', sep='\t', header=True)")

sql_query = """
WITH pnr_load_pnr_level AS (
    SELECT
        company_id,
        flight_number,
        scheduled_departure_date_local,
        record_locator,
        MAX(total_pax) AS pnr_size
    FROM pnr_flight_level_data
    GROUP BY 1, 2, 3, 4
),
passenger_load_flight_level AS (
    SELECT
        company_id,
        flight_number,
        scheduled_departure_date_local,
        SUM(pnr_size) AS Total_Passengers
    FROM pnr_load_pnr_level
    GROUP BY 1, 2, 3
),
operational_data AS (
    SELECT
    //Note: In DuckDB, to handle the column name 's', you might need to use quotes if it wasn't renamed during file loading.//
        s AS company_id,
        flight_number,
        scheduled_departure_date_local,
        total_seats,
        (actual_departure_datetime_local::TIMESTAMP - scheduled_departure_datetime_local::TIMESTAMP) / 1000000 / 60.0 AS Departure_Delay_Minutes,
        (actual_ground_time_minutes - minimum_turn_minutes) AS Ground_Time_Difficulty_Minutes
    FROM flight_level_data
)
SELECT
    O.company_id,
    O.flight_number,
    O.scheduled_departure_date_local,
    O.total_seats,
    P.Total_Passengers,
    O.Departure_Delay_Minutes,
    O.Ground_Time_Difficulty_Minutes,
    CAST(P.Total_Passengers AS REAL) / O.total_seats AS Load_Factor
FROM operational_data AS O
INNER JOIN passenger_load_flight_level AS P
    ON O.company_id = P.company_id
    AND O.flight_number = P.flight_number
    AND O.scheduled_departure_date_local = P.scheduled_departure_date_local;
"""
df_result = con.execute(sql_query).fetchdf()

print(df_result.head())
# Remember to close the connection
con.close()