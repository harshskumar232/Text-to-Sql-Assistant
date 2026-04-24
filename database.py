import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("sales.db")

# Load the real Superstore dataset
df = pd.read_csv("superstore.csv", encoding="latin1")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

print("Columns:", df.columns.tolist())
print("Rows:", len(df))

# Save to SQLite
df.to_sql("sales", conn, if_exists="replace", index=False)

print("\nDatabase loaded successfully!")
print(df.head(3))

conn.close()