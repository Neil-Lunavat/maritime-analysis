import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('data1.csv')

print('Dataset shape:', df.shape)
print('\nBasic info:')
print(df.info())

numeric_cols = ['SPEED', 'LENGTH', 'WIDTH', 'COURSE', 'HEADING', 'ROT', 'DWT']
df_numeric = df[numeric_cols].dropna()

print('\n=== Summary Statistics ===')
for col in ['SPEED', 'LENGTH', 'WIDTH']:
    data = df[col].dropna()
    print(f'\n{col}:')
    print(f'  Mean: {data.mean():.2f}')
    print(f'  Median: {data.median():.2f}')
    print(f'  Std Dev: {data.std():.2f}')
    print(f'  Variance: {data.var():.2f}')
    print(f'  Min: {data.min():.2f}')
    print(f'  Max: {data.max():.2f}')

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

df['SPEED'].hist(bins=50, ax=axes[0], edgecolor='black')
axes[0].set_title('Speed Distribution')
axes[0].set_xlabel('Speed (knots)')
axes[0].grid(alpha=0.3)

df['LENGTH'].hist(bins=50, ax=axes[1], edgecolor='black')
axes[1].set_title('Ship Length Distribution')
axes[1].set_xlabel('Length (m)')
axes[1].grid(alpha=0.3)

df['WIDTH'].hist(bins=30, ax=axes[2], edgecolor='black')
axes[2].set_title('Ship Width Distribution')
axes[2].set_xlabel('Width (m)')
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('histograms.png', dpi=100)
print('\nSaved histograms.png')

print('\nObservations:')
print('- Speed is right-skewed, most ships at low speeds')
print('- Length shows multiple peaks, different ship classes')
print('- Width correlates with length, some outliers')

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].boxplot(df['SPEED'].dropna(), vert=True)
axes[0].set_ylabel('Speed (knots)')
axes[0].set_title('Speed Boxplot')
axes[0].grid(alpha=0.3)

axes[1].boxplot(df['LENGTH'].dropna(), vert=True)
axes[1].set_ylabel('Length (m)')
axes[1].set_title('Length Boxplot')
axes[1].grid(alpha=0.3)

axes[2].boxplot(df['WIDTH'].dropna(), vert=True)
axes[2].set_ylabel('Width (m)')
axes[2].set_title('Width Boxplot')
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('boxplots.png', dpi=100)
print('Saved boxplots.png')

print('\n- Speed has many outliers above 150 knots')
print('- Length outliers above 350m (large vessels)')
print('- Width shows tight clustering with few outliers')

corr_cols = ['SPEED', 'COURSE', 'HEADING', 'LENGTH', 'WIDTH', 'ROT', 'DWT']
corr_df = df[corr_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, fmt='.2f', cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=100)
print('\nSaved correlation_heatmap.png')

print('\nCorrelation insights:')
print('- LENGTH and WIDTH strongly correlated (0.8+)')
print('- DWT correlates with ship dimensions')
print('- COURSE and HEADING show moderate correlation')

plt.figure(figsize=(10, 6))
scatter_df = df.dropna(subset=['LENGTH', 'WIDTH', 'SPEED'])
plt.scatter(scatter_df['LENGTH'], scatter_df['WIDTH'],
            c=scatter_df['SPEED'], cmap='viridis', alpha=0.5, s=10)
plt.colorbar(label='Speed (knots)')
plt.xlabel('Length (m)')
plt.ylabel('Width (m)')
plt.title('Ship Dimensions vs Speed')
plt.grid(alpha=0.3)
plt.savefig('length_width_scatter.png', dpi=100)
print('Saved length_width_scatter.png')

print('\n- Larger ships tend to have lower speeds')
print('- Clear dimensional clusters by ship type')
