import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             roc_curve, auc, classification_report)
import warnings
warnings.filterwarnings('ignore')

# Load the cleaned data
print("Loading cleaned dataset...")
df = pd.read_csv('/Users/armansarrafi/Downloads/datacleanfinal.csv')

print(f"Dataset shape: {df.shape}")
print(f"\nTarget variable distribution:\n{df['target'].value_counts()}")
print(f"\nMissing values:\n{df.isnull().sum().sum()}")

# Separate features and target
X = df.drop('target', axis=1)
y = df['target']

# Handle categorical variables with one-hot encoding
print("\nEncoding categorical variables...")
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"Categorical columns: {categorical_cols}")

if categorical_cols:
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    print(f"Features shape after encoding: {X.shape}")

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split data into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")
print(f"Train target distribution:\n{y_train.value_counts()}")
print(f"Test target distribution:\n{y_test.value_counts()}")

# Scale the features
print("\nScaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

# Store results
results = {}
predictions = {}

# Train and evaluate each model
print("\n" + "="*80)
print("MODEL TRAINING AND EVALUATION")
print("="*80)

for model_name, model in models.items():
    print(f"\n\nTraining {model_name}...")

    # Use scaled data for Logistic Regression, original for tree-based models
    if model_name == 'Logistic Regression':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Store predictions
    predictions[model_name] = {
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Cross-validation
    if model_name == 'Logistic Regression':
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')

    results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }

    print(f"\n{model_name} Results:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"  ROC-AUC:   {roc_auc:.4f}")
    print(f"  CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    print(f"\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Readmission (<30)', 'Readmission (<30)']))

# Create results DataFrame
results_df = pd.DataFrame(results).T
print("\n\n" + "="*80)
print("SUMMARY COMPARISON")
print("="*80)
print(results_df.to_string())

# Save results to CSV
results_df.to_csv('/Users/armansarrafi/Downloads/model_results.csv')
print("\nResults saved to: /Users/armansarrafi/Downloads/model_results.csv")

# Visualizations
print("\nGenerating visualizations...")

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')

# 1. Metrics Comparison
ax1 = axes[0, 0]
metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
x = np.arange(len(models))
width = 0.15

for i, metric in enumerate(metrics):
    values = [results[model][metric] for model in models.keys()]
    ax1.bar(x + i*width, values, width, label=metric.upper())

ax1.set_xlabel('Models', fontweight='bold')
ax1.set_ylabel('Score', fontweight='bold')
ax1.set_title('Model Metrics Comparison')
ax1.set_xticks(x + width * 2)
ax1.set_xticklabels(models.keys(), rotation=15, ha='right')
ax1.legend(fontsize=8)
ax1.set_ylim([0, 1])
ax1.grid(axis='y', alpha=0.3)

# 2. ROC Curves
ax2 = axes[0, 1]
for model_name in models.keys():
    fpr, tpr, _ = roc_curve(y_test, predictions[model_name]['y_pred_proba'])
    roc_auc = results[model_name]['roc_auc']
    ax2.plot(fpr, tpr, label=f"{model_name} (AUC={roc_auc:.3f})", linewidth=2)

ax2.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
ax2.set_xlabel('False Positive Rate', fontweight='bold')
ax2.set_ylabel('True Positive Rate', fontweight='bold')
ax2.set_title('ROC Curves')
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

# 3. Confusion Matrices
ax3 = axes[1, 0]
best_model = max(results.keys(), key=lambda x: results[x]['roc_auc'])
cm = confusion_matrix(y_test, predictions[best_model]['y_pred'])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax3,
            xticklabels=['No Readmission', 'Readmission'],
            yticklabels=['No Readmission', 'Readmission'])
ax3.set_title(f'Confusion Matrix - {best_model} (Best Model)')
ax3.set_ylabel('True Label', fontweight='bold')
ax3.set_xlabel('Predicted Label', fontweight='bold')

# 4. Cross-validation scores
ax4 = axes[1, 1]
cv_means = [results[model]['cv_mean'] for model in models.keys()]
cv_stds = [results[model]['cv_std'] for model in models.keys()]
x = np.arange(len(models))
ax4.bar(x, cv_means, yerr=cv_stds, capsize=5, alpha=0.7, color='steelblue')
ax4.set_xlabel('Models', fontweight='bold')
ax4.set_ylabel('CV ROC-AUC Score', fontweight='bold')
ax4.set_title('5-Fold Cross-Validation Results')
ax4.set_xticks(x)
ax4.set_xticklabels(models.keys(), rotation=15, ha='right')
ax4.set_ylim([0, 1])
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/armansarrafi/Downloads/model_evaluation.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: /Users/armansarrafi/Downloads/model_evaluation.png")

# Feature importance for Random Forest (best tree-based model)
print("\n\nExtracting feature importance from Random Forest...")
rf_model = models['Random Forest']
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 20 Most Important Features:")
print(feature_importance.head(20).to_string(index=False))

# Plot feature importance
fig, ax = plt.subplots(figsize=(10, 8))
top_features = feature_importance.head(20)
ax.barh(range(len(top_features)), top_features['importance'])
ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['feature'])
ax.set_xlabel('Feature Importance', fontweight='bold')
ax.set_title('Top 20 Most Important Features - Random Forest', fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('/Users/armansarrafi/Downloads/feature_importance.png', dpi=300, bbox_inches='tight')
print("\nFeature importance plot saved to: /Users/armansarrafi/Downloads/feature_importance.png")

# Save feature importance to CSV
feature_importance.to_csv('/Users/armansarrafi/Downloads/feature_importance.csv', index=False)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Best performing model: {best_model}")
print(f"Best ROC-AUC Score: {results[best_model]['roc_auc']:.4f}")
print(f"Test Accuracy: {results[best_model]['accuracy']:.4f}")
print(f"Test Precision: {results[best_model]['precision']:.4f}")
print(f"Test Recall: {results[best_model]['recall']:.4f}")
print(f"Test F1-Score: {results[best_model]['f1']:.4f}")

print("\nAll output files saved to: /Users/armansarrafi/Downloads/")
print("  - model_results.csv")
print("  - model_evaluation.png")
print("  - feature_importance.png")
print("  - feature_importance.csv")
