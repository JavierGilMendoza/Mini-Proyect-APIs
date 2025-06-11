import os
import pandas as pd

# Define cleaned data path
cleaned_data_path = os.path.join("data", "clean")
output_path = os.path.join("data", "merged", "all_seasons.csv")

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# List to collect individual DataFrames
dataframes = []

# Loop through all cleaned CSV files
for file in sorted(os.listdir(cleaned_data_path)):
    if file.endswith(".csv"):
        print(f"Reading: {file}")
        file_path = os.path.join(cleaned_data_path, file)
        df = pd.read_csv(file_path, parse_dates=["date"])
        df["season"] = file.replace(".csv", "")  # Add season identifier
        dataframes.append(df)

# Concatenate all DataFrames
merged_df = pd.concat(dataframes, ignore_index=True)

# Save to a single CSV file
merged_df.to_csv(output_path, index=False)
print(f"\n✅ All seasons merged into: {output_path}")