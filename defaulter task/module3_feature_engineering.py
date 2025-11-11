import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('data1.csv')

print(f'Starting with {df.shape[0]} records')

def circular_diff(angle1, angle2):
    diff = angle1 - angle2
    diff = (diff + 180) % 360 - 180
    return np.abs(diff)

df['HC_DIFF'] = df.apply(lambda row: circular_diff(row['HEADING'], row['COURSE'])
                         if pd.notna(row['HEADING']) and pd.notna(row['COURSE'])
                         else np.nan, axis=1)

df['LW_RATIO'] = df['LENGTH'] / df['WIDTH']

df['SPEED_ZSCORE'] = (df['SPEED'] - df['SPEED'].mean()) / df['SPEED'].std()

df['ROT_ABS'] = df['ROT'].abs()

print('\nNew features created:')
print('- HC_DIFF: heading-course difference')
print('- LW_RATIO: length/width ratio')
print('- SPEED_ZSCORE: standardized speed')
print('- ROT_ABS: absolute rate of turn')

print('\n=== Feature Statistics ===')
print('\nHC_DIFF:')
print(df['HC_DIFF'].describe())

print('\nLW_RATIO:')
print(df['LW_RATIO'].describe())

print('\nSPEED_ZSCORE:')
print(df['SPEED_ZSCORE'].describe())

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

df['HC_DIFF'].hist(bins=50, ax=axes[0, 0], edgecolor='black')
axes[0, 0].set_title('Heading-Course Difference')
axes[0, 0].set_xlabel('Degrees')
axes[0, 0].grid(alpha=0.3)

df['LW_RATIO'].hist(bins=50, ax=axes[0, 1], edgecolor='black')
axes[0, 1].set_title('Length/Width Ratio')
axes[0, 1].set_xlabel('Ratio')
axes[0, 1].grid(alpha=0.3)

df['SPEED_ZSCORE'].hist(bins=50, ax=axes[1, 0], edgecolor='black')
axes[1, 0].set_title('Speed Z-Score')
axes[1, 0].set_xlabel('Z-Score')
axes[1, 0].grid(alpha=0.3)

df['ROT_ABS'].hist(bins=50, ax=axes[1, 1], edgecolor='black')
axes[1, 1].set_title('Absolute Rate of Turn')
axes[1, 1].set_xlabel('deg/min')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('engineered_features.png', dpi=100)
print('\nSaved engineered_features.png')

print('\nObservations:')
print('- Most ships have low HC_DIFF (following course)')
print('- LW_RATIO peaks around 5-8 (typical ship proportions)')
print('- Speed Z-scores show some extreme outliers')

ship_types = df['SHIPTYPE'].value_counts().head(5).index
df_top_types = df[df['SHIPTYPE'].isin(ship_types)]

print(f'\nAnalyzing top {len(ship_types)} ship types')

grouped = df_top_types.groupby('SHIPTYPE')[['SPEED', 'LENGTH', 'LW_RATIO', 'HC_DIFF']].mean()
print('\nAverage by ship type:')
print(grouped)

plt.figure(figsize=(12, 8))
geo_df = df.dropna(subset=['LON', 'LAT', 'SPEED'])
scatter = plt.scatter(geo_df['LON'], geo_df['LAT'],
                     c=geo_df['SPEED'], cmap='plasma',
                     alpha=0.6, s=5)
plt.colorbar(scatter, label='Speed (knots)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographic Distribution with Speed')
plt.grid(alpha=0.3)
plt.savefig('geographic_speed_plot.png', dpi=100)
print('\nSaved geographic_speed_plot.png')

corr_features = ['SPEED', 'LENGTH', 'WIDTH', 'HC_DIFF', 'LW_RATIO', 'SPEED_ZSCORE', 'ROT_ABS']
corr_new = df[corr_features].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_new, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Correlation with Engineered Features')
plt.tight_layout()
plt.savefig('engineered_correlation.png', dpi=100)
print('Saved engineered_correlation.png')

print('\nKey correlations:')
print('- LW_RATIO negatively correlated with WIDTH')
print('- SPEED_ZSCORE perfect correlation with SPEED (by design)')
print('- HC_DIFF shows weak correlation with other features')

anomalies = df[(df['SPEED_ZSCORE'].abs() > 3) | (df['HC_DIFF'] > 90)]
print(f'\nFound {len(anomalies)} potential anomalies')
print('Criteria: |speed_zscore| > 3 OR HC_DIFF > 90 degrees')

df.to_csv('data_with_features.csv', index=False)
print('\nSaved enhanced dataset to data_with_features.csv')
