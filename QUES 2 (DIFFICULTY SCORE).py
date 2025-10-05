# Difficulty score calculation
import pandas as pd
import numpy as np

df = pd.read_csv('flight_difficulty_features.csv')

df['ground_time_overrun'] = np.maximum(0, df['actual_ground_time_minutes'] - df['minimum_turn_minutes'])

df['positive_departure_delay_minutes'] = np.maximum(0, df['departure_delay_minutes'])

score_features = [
    'ground_time_overrun',
    'total_ssr_count',
    'positive_departure_delay_minutes',
    'total_checked_bags',
    'load_factor'
]

GROUP_COLUMN = 'scheduled_departure_date_local'

for feature in score_features:
    mean_val = df.groupby(GROUP_COLUMN)[feature].transform('mean')
    std_val = df.groupby(GROUP_COLUMN)[feature].transform('std')

    # Calculate Z-score: (X - mu) / sigma
    # Z-scores are stored in new columns prefixed with 'Z_'
    z_score_col = f'Z_{feature}'
    
    df[z_score_col] = (df[feature] - mean_val) / std_val
    
    df[z_score_col] = df[z_score_col].fillna(0)


weights = {
    'Z_ground_time_overrun': 0.40,
    'Z_total_ssr_count': 0.30,
    'Z_positive_departure_delay_minutes': 0.15,
    'Z_total_checked_bags': 0.10,
    'Z_load_factor': 0.05
}

df['Difficulty_Score'] = (
    df['Z_ground_time_overrun'] * weights['Z_ground_time_overrun'] +
    df['Z_total_ssr_count'] * weights['Z_total_ssr_count'] +
    df['Z_positive_departure_delay_minutes'] * weights['Z_positive_departure_delay_minutes'] +
    df['Z_total_checked_bags'] * weights['Z_total_checked_bags'] +
    df['Z_load_factor'] * weights['Z_load_factor']
)


df['Daily_Difficulty_Rank'] = df.groupby(GROUP_COLUMN)['Difficulty_Score'].rank(method='min', ascending=False)

daily_quartiles = df.groupby(GROUP_COLUMN)['Difficulty_Score'].quantile([0.25, 0.75]).unstack()

df = df.merge(daily_quartiles, on=GROUP_COLUMN, suffixes=('_0_25', '_0_75'))

def classify_difficulty(row):
    score = row['Difficulty_Score']
    q_25 = row[0.25]
    q_75 = row[0.75]
    
    if score >= q_75:
        return 'Difficult'
    elif score >= q_25:
        return 'Medium'
    else:
        return 'Easy'

df['Difficulty_Category'] = df.apply(classify_difficulty, axis=1)


output_columns = [
    'scheduled_departure_date_local',
    'company_id',
    'flight_number',
    'Difficulty_Score',
    'Daily_Difficulty_Rank',
    'Difficulty_Category'
]

df_output = df[output_columns].sort_values(by=[GROUP_COLUMN, 'Daily_Difficulty_Rank'], ascending=[True, True])

df_output.to_csv('flight_difficulty_scored_output.csv', index=False)