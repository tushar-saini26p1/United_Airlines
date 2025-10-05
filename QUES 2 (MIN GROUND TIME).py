import pandas as pd

try:
    df = pd.read_csv("Flight Level Data.csv", sep='\t')
except FileNotFoundError:
    print("Error: 'Flight Level Data.csv' not found. Please ensure the file is in the correct path.")
    exit()     # 'Flight Level Data.csv' is the file name of data it is.

scheduled_ground_col = 'scheduled_ground_time_minutes'
minimum_turn_col = 'minimum_turn_minutes'

df[scheduled_ground_col] = pd.to_numeric(df[scheduled_ground_col], errors='coerce')
df[minimum_turn_col] = pd.to_numeric(df[minimum_turn_col], errors='coerce')
df.dropna(subset=[scheduled_ground_col, minimum_turn_col], inplace=True)

close_to_or_below_turn_mins_df = df[
    df[scheduled_ground_col] <= df[minimum_turn_col]
]

count = close_to_or_below_turn_mins_df.shape[0]

print(f"Total number of flights: {len(df)}")
print(f"Number of flights with scheduled ground time close to or below minimum turn minutes: {count}")