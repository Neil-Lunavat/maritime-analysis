import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data1.csv')

print('=== REGRESSION TASK: Predicting Speed ===\n')

reg_df = df[['SPEED', 'LENGTH', 'WIDTH', 'SHIPTYPE', 'ROT', 'COURSE']].dropna()
print(f'Dataset size: {len(reg_df)} records')

X_reg = reg_df[['LENGTH', 'WIDTH', 'SHIPTYPE', 'ROT', 'COURSE']]
y_reg = reg_df['SPEED']

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.3, random_state=42
)

lr_model = LinearRegression()
lr_model.fit(X_train_reg, y_train_reg)

y_pred_reg = lr_model.predict(X_test_reg)

r2 = r2_score(y_test_reg, y_pred_reg)
mae = mean_absolute_error(y_test_reg, y_pred_reg)

print(f'R² Score: {r2:.4f}')
print(f'Mean Absolute Error: {mae:.2f} knots')

print('\nSample predictions:')
sample = pd.DataFrame({
    'Actual': y_test_reg.values[:10],
    'Predicted': y_pred_reg[:10]
})
print(sample)

plt.figure(figsize=(10, 6))
plt.scatter(y_test_reg, y_pred_reg, alpha=0.5, s=10)
plt.plot([y_test_reg.min(), y_test_reg.max()],
         [y_test_reg.min(), y_test_reg.max()],
         'r--', lw=2)
plt.xlabel('Actual Speed')
plt.ylabel('Predicted Speed')
plt.title(f'Linear Regression: Speed Prediction (R²={r2:.3f})')
plt.grid(alpha=0.3)
plt.savefig('regression_results.png', dpi=100)
print('\nSaved regression_results.png')

print('\n' + '='*50)
print('=== CLASSIFICATION TASK: Ship Type Classification ===\n')

class_df = df[['SHIPTYPE', 'LENGTH', 'WIDTH', 'SPEED', 'ROT']].dropna()

top_types = class_df['SHIPTYPE'].value_counts().head(3).index
class_df = class_df[class_df['SHIPTYPE'].isin(top_types)]
print(f'Classifying top 3 ship types: {list(top_types)}')
print(f'Dataset size: {len(class_df)} records')

X_class = class_df[['LENGTH', 'WIDTH', 'SPEED', 'ROT']]
y_class = class_df['SHIPTYPE']

X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(
    X_class, y_class, test_size=0.3, random_state=42, stratify=y_class
)

print('\n--- Logistic Regression ---')
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train_class, y_train_class)
y_pred_log = log_model.predict(X_test_class)

log_acc = accuracy_score(y_test_class, y_pred_log)
print(f'Accuracy: {log_acc:.4f}')

print('\nConfusion Matrix:')
print(confusion_matrix(y_test_class, y_pred_log))

print('\nClassification Report:')
print(classification_report(y_test_class, y_pred_log))

print('\n--- Decision Tree Classifier ---')
dt_model = DecisionTreeClassifier(max_depth=10, random_state=42)
dt_model.fit(X_train_class, y_train_class)
y_pred_dt = dt_model.predict(X_test_class)

dt_acc = accuracy_score(y_test_class, y_pred_dt)
print(f'Accuracy: {dt_acc:.4f}')

print('\nConfusion Matrix:')
print(confusion_matrix(y_test_class, y_pred_dt))

print('\n--- KNN Classifier ---')
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_class, y_train_class)
y_pred_knn = knn_model.predict(X_test_class)

knn_acc = accuracy_score(y_test_class, y_pred_knn)
print(f'Accuracy: {knn_acc:.4f}')

print('\n' + '='*50)
print('=== MODEL COMPARISON ===\n')

results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Decision Tree', 'KNN'],
    'Accuracy': [log_acc, dt_acc, knn_acc]
})
print(results)

best_model = results.loc[results['Accuracy'].idxmax(), 'Model']
best_acc = results['Accuracy'].max()
print(f'\nBest model: {best_model} with {best_acc:.4f} accuracy')

if best_model == 'Decision Tree':
    print('Decision Tree performs well likely due to non-linear decision boundaries')
elif best_model == 'KNN':
    print('KNN works well when ship types cluster by features')
else:
    print('Logistic Regression shows linear separability works for this task')

plt.figure(figsize=(8, 5))
plt.bar(results['Model'], results['Accuracy'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.ylabel('Accuracy')
plt.title('Classification Model Comparison')
plt.ylim(0, 1)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(results['Accuracy']):
    plt.text(i, v + 0.02, f'{v:.3f}', ha='center')
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=100)
print('\nSaved model_comparison.png')
