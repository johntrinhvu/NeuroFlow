import pandas as pd
import numpy as np

def extract_heart_rate_features(input_csv, window_size=5):
    """
    Extract heart rate features from input CSV
    
    Parameters:
    -----------
    input_csv : str
        Path to input CSV file
    window_size : int, optional
        Size of rolling window for calculations (default 5)
    
    Returns:
    --------
    DataFrame with additional feature columns
    """
    # Read the CSV
    df = pd.read_csv(input_csv)
    
    # Sort by time to ensure correct calculations
    df = df.sort_values('time')
    
    # Calculate rolling mean and standard deviation
    df['rolling_mean'] = df['value'].rolling(window=window_size, center=True, min_periods=1).mean()
    df['rolling_std'] = df['value'].rolling(window=window_size, center=True, min_periods=1).std()
    
    # Calculate rate of change
    df['rate_of_change'] = df['value'].diff()
    
    # Calculate relative change percentage
    df['relative_change_pct'] = df['value'].pct_change() * 100
    
    # # Calculate baseline and stress period statistics
    # df['baseline_mean'] = df[df['classification'] == 0]['value'].mean()
    # df['stress_mean'] = df[df['classification'] == 1]['value'].mean()
    # df['baseline_std'] = df[df['classification'] == 0]['value'].std()
    # df['stress_std'] = df[df['classification'] == 1]['value'].std()
    
    return df

# Example usage
def main():
    input_path = 's2_stress_data.csv'
    output_df = extract_heart_rate_features(input_path)
    output_path = 's2_stress_data_with_features.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Features extracted and saved to {output_path}")

if __name__ == "__main__":
    main()