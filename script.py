import json
import os
import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    file_names = ["station_00.json", "station_01.json", "station_10.json", "station_11.json"]
    
    all_rows = []
    
    for file_path in file_names:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                rows = data["data"]["rows"]
                all_rows.extend(rows)
                print(f"Loaded {len(rows)} records from {file_path}")
        else:
            print(f"Warning: {file_path} not found")
    
    if all_rows:
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(all_rows)
        df.to_csv("output.csv", index=False)
        print(f"Converted {len(all_rows)} total records to output.csv")
    else:
        print("No data found in any files")