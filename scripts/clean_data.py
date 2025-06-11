import os
import pandas as pd

# Define paths for raw and cleaned data
raw_data_path = os.path.join("data", "raw")
cleaned_data_path = os.path.join("data", "clean")

# Create cleaned directory if it doesn't exist
os.makedirs(cleaned_data_path, exist_ok=True)

# Dictionary for replacing incorrect team names
team_name_corrections = {
    "Espanol": "Español",
    "La Coruna": "La Coruña",
    "Logrones": "Logroñes",
    "Villareal": "Villarreal"
}

# Mapping for FTR column replacement
ftr_mapping = {"H": "1", "D": "X", "A": "2"}

# Loop through all CSV files in the raw data folder
for file in os.listdir(raw_data_path):
    if file.endswith(".csv"):
        print(f"Processing: {file}")
        try:
            # Load only selected columns: Date, HomeTeam, AwayTeam, FTR
            df = pd.read_csv(
                os.path.join(raw_data_path, file),
                usecols=["Date", "HomeTeam", "AwayTeam", "FTR"],
                encoding="utf-8",
                on_bad_lines="warn"  # Skip malformed lines
            )
        except UnicodeDecodeError:
            # Try alternative encoding if UTF-8 fails
            df = pd.read_csv(
                os.path.join(raw_data_path, file),
                usecols=["Date", "HomeTeam", "AwayTeam", "FTR"],
                encoding="latin-1",
                on_bad_lines="warn"
            )
        except Exception as e:
            print(f"Failed to process {file}: {e}")
            continue

        # Normalize column names
        df.columns = [col.strip().lower() for col in df.columns]

        # Convert date column
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

        # Drop rows with missing values
        df.dropna(subset=["date", "hometeam", "awayteam", "ftr"], inplace=True)

        # Replace incorrect team names
        df["hometeam"] = df["hometeam"].replace(team_name_corrections)
        df["awayteam"] = df["awayteam"].replace(team_name_corrections)

        # Replace FTR values with numeric codes
        df["ftr"] = df["ftr"].replace(ftr_mapping)

        # Save cleaned file
        df.to_csv(os.path.join(cleaned_data_path, file), index=False)
