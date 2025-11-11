import pandas as pd
import numpy as np
import json

df = pd.read_csv('data1.csv')

print(f'Original shape: {df.shape}')
print(df.dtypes)

print('\nMissing values:')
print(df.isnull().sum())

df['ROT'].fillna(0, inplace=True)

initial_rows = len(df)
df = df.dropna(subset=['LAT', 'LON', 'SPEED'])
print(f'\nDropped {initial_rows - len(df)} rows with missing critical data')

print(f'\nDuplicates: {df.duplicated().sum()}')
df = df.drop_duplicates()

df_filtered = df[df['SPEED'] > 0].copy()
print(f'Removed {len(df) - len(df_filtered)} zero-speed entries')

q99 = df_filtered['SPEED'].quantile(0.99)
df_filtered = df_filtered[df_filtered['SPEED'] <= q99]
print(f'Filtered speed outliers above {q99:.1f}')

print(f'\nFinal shape: {df_filtered.shape}')

df_filtered.to_csv('cleaned_data.csv', index=False)
print('Saved to cleaned_data.csv')

data_dict = df_filtered.to_dict(orient='records')
with open('ship_data.json', 'w') as f:
    json.dump(data_dict[:100], f, indent=2)
print('Saved first 100 records to ship_data.json')

print('\nCleaned data summary:')
print(df_filtered.describe())
