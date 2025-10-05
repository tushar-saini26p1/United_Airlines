import pandas as pd

# Define the file
file_name = 'Flight Level Data.csv'
delimiter = '\t' 

df = pd.read_csv(file_name, sep=delimiter)

df['scheduled_departure_datetime_local'] = pd.to_datetime(df['scheduled_departure_datetime_local'])
df['actual_departure_datetime_local'] = pd.to_datetime(df['actual_departure_datetime_local']) # Convert scheduled and actual departure times to datetime objects

# Delay is calculated as: Actual Time - Scheduled Time
delay = (
    df['actual_departure_datetime_local'] - df['scheduled_departure_datetime_local']
).dt.total_seconds() / 60

average_delay = delay.mean() # Calculate the Average Delay

total_flights = len(df)
delayed_flights_count = (delay > 0).sum()
percentage_departed_later = (delayed_flights_count / total_flights) * 100    # Calculate the Percentage of Delayed Flights (departing later than scheduled, delay > 0)

print(f"Average Departure Delay: {average_delay:.2f} minutes")
print(f"Percentage of Flights Departing Later than Scheduled: {percentage_departed_later:.2f}%")