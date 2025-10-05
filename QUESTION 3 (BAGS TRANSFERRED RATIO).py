import pandas as pd
import numpy as np

df = pd.read_csv("Bag+Level+Data.csv", sep='\t')

df['flight_id'] = df['flight_number'].astype(str) + '_' + df['scheduled_departure_date_local']

df['is_transfer'] = np.where(df['bag_type'].isin(['Transfer', 'Hot Transfer']), 1, 0)
df['is_origin'] = np.where(df['bag_type'] == 'Origin', 1, 0)

bag_counts_by_flight = df.groupby('flight_id').agg(
    total_transfer_bags=('is_transfer', 'sum'),
    total_origin_bags=('is_origin', 'sum')
).reset_index()

bag_counts_by_flight['transfer_vs_origin_ratio'] = (
    bag_counts_by_flight['total_transfer_bags'] / bag_counts_by_flight['total_origin_bags']
)

ratio_series = bag_counts_by_flight['transfer_vs_origin_ratio'].replace([np.inf, -np.inf], np.nan).dropna()

average_ratio = ratio_series.mean()

print(f"Average Ratio of Transfer Bags vs. Origin Bags across all flights: {average_ratio:.4f}")