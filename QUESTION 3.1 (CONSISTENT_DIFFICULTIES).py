import pandas as pd

def analyze_destination_difficulty_by_airline(file_path):
    """
    Loads flight data, groups by destination and airline, and calculates 
    average difficulty-related metrics.
    
    Args:
        file_path (str): The path to the flight data CSV file.
        
    Returns:
        pd.DataFrame: A DataFrame showing the mean difficulty metrics 
                      for each destination-airline pair.
    """
    # Load the flight data
    df = pd.read_csv(file_path)
    
    # Select the relevant columns
    cols_of_interest = [
        'scheduled_arrival_station_code', 
        'company_id', 
        'total_ssr_count', 
        'load_factor', 
        'transfer_bag_ratio',
        'minimum_turn_minutes'
    ]
    df_subset = df[cols_of_interest]
    
    # Group by destination and airline and calculate the mean of the metrics
    grouped_analysis = df_subset.groupby([
        'scheduled_arrival_station_code', 
        'company_id'
    ]).mean().reset_index()
    
    # Rename columns for clarity
    grouped_analysis.columns = [
        'Destination', 
        'Airline', 
        'Avg Total SSR Count', 
        'Avg Load Factor', 
        'Avg Transfer Bag Ratio',
        'Avg Minimum Turn Time (min)'
    ]
    
    # Sort the results by Destination and then by Avg Total SSR Count (descending)
    grouped_analysis = grouped_analysis.sort_values(
        by=['Destination', 'Avg Total SSR Count'], 
        ascending=[True, False]
    )
    
    return grouped_analysis

# Call the function with the appropriate file
analysis_result = analyze_destination_difficulty_by_airline('flight_difficulty_features.csv')

# Print the top 20 rows of the resulting DataFrame
print(analysis_result.head(20).to_markdown(index=False, numalign="left", stralign="left"))