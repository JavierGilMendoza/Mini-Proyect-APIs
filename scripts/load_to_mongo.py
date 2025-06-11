import pandas as pd
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Change if using another URI
db = client["futbol_db"]
collection = db["matches"]

# Read CSV file
df = pd.read_csv("data/merged/all_seasons.csv")

# Convert DataFrame to dictionaries (list of documents)
records = df.to_dict(orient="records")

# Clear collection before inserting (optional)
collection.delete_many({})

# Insert data into MongoDB
collection.insert_many(records)

print(f"Inserted {len(records)} documents into MongoDB.")