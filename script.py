import json
import os
import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    file_path = "station.json"  # Replace with your JSON file path
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    rows = data["data"]["rows"]
    if rows:
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(rows)
        df.to_csv("output.csv", index=False)
        print(f"Converted {len(rows)} records to output.csv")
