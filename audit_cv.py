import pickle
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler

with open('phase1_outputs/phase1_data.pkl', 'rb') as f:
    p1 = pickle.load(f)

X_train = p1['X_train']
y_train = p1['y_train']

with open('results/chosen_model_bundle.pkl', 'rb') as f:
    bundle = pickle.load(f)
mask_fi = bundle['mask_fi']
X_train_sel = X_train[:, mask_fi]

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Strict leak-free pipeline: UnderSampling applied ONLY to training folds, validation folds kept natural (22.4% prevalence)
pipe_rf = Pipeline([
    ('rus', RandomUnderSampler(random_state=42)),
    ('clf', RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=5, min_samples_split=10, random_state=42, n_jobs=-1))
])

pipe_dt = Pipeline([
    ('rus', RandomUnderSampler(random_state=42)),
    ('clf', DecisionTreeClassifier(max_depth=10, min_samples_leaf=5, min_samples_split=10, random_state=42))
])

scoring = ['recall', 'precision', 'roc_auc', 'accuracy', 'f1']

res_rf = cross_validate(pipe_rf, X_train_sel, y_train, cv=cv, scoring=scoring)
res_dt = cross_validate(pipe_dt, X_train_sel, y_train, cv=cv, scoring=scoring)

print("=== STRICT LEAK-FREE 10-FOLD CV (Validation folds at natural 22.4% prevalence) ===")
print(f"RF: Recall = {res_rf['test_recall'].mean():.4f}, Precision = {res_rf['test_precision'].mean():.4f}, ROC-AUC = {res_rf['test_roc_auc'].mean():.4f}, F1 = {res_rf['test_f1'].mean():.4f}")
print(f"DT: Recall = {res_dt['test_recall'].mean():.4f}, Precision = {res_dt['test_precision'].mean():.4f}, ROC-AUC = {res_dt['test_roc_auc'].mean():.4f}, F1 = {res_dt['test_f1'].mean():.4f}")

