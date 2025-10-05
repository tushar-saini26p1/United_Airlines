import pandas as pd
import numpy as np

FLIGHT_FILE = "Flight Level Data.csv"
PNR_FLIGHT_FILE = "PNR+Flight+Level+Data.csv"
PNR_REMARK_FILE = "PNR Remark Level Data.csv"

flight_df = pd.read_csv(FLIGHT_FILE)
pnr_flight_df = pd.read_csv(PNR_FLIGHT_FILE)
pnr_remark_df = pd.read_csv(PNR_REMARK_FILE)

KEY_COLS = ['company_id', 'flight_number', 'scheduled_departure_date_local']
PNR_KEY_COLS = ['record_locator', 'flight_number']


cols_to_select = ['record_locator', 'flight_number', 'company_id', 'scheduled_departure_date_local']
ssr_key_map = pnr_flight_df[cols_to_select].drop_duplicates()

ssr_merge_df = pd.merge(
    pnr_remark_df,
    ssr_key_map,
    on=PNR_KEY_COLS,
    how='inner'
)

HIGH_LOAD_THRESHOLD = 0.8
ssr_threshold = final_df['ssr_count'].quantile(0.75)
ssr_threshold = max(1, ssr_threshold) # Set 'High SSR' threshold (3.0 in this run)

final_df['load_category'] = np.where(
    final_df['load_factor'] >= HIGH_LOAD_THRESHOLD,
    'High Load',
    'Low Load'
)
final_df['ssr_category'] = np.where(
    final_df['ssr_count'] >= ssr_threshold,
    'High SSR',
    'Low SSR'
)

comparison_results = final_df.groupby(['load_category', 'ssr_category'])['departure_delay_minutes'].mean().reset_index(name='avg_departure_delay_minutes')