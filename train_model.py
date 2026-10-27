
"""
Car Resale Price Prediction - Model Training Script
====================================================
Trains three models:
  1. Linear Regression
  2. Random Forest Regressor
  3. Decision Tree Regressor

Saves trained models + the scaler + column list to /models/
"""

import datetime
import pickle
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ─── 1. Load Dataset ────────────────────────────────────────────────────────
print("=" * 60)
print("  Car Resale Price Predictor – Training Pipeline")
print("=" * 60)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset.csv")
df = pd.read_csv(DATA_PATH)

print(f"\n[1] Dataset loaded → {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head(3).to_string())

# ─── 2. Drop rows where target is missing ───────────────────────────────────
df = df.dropna(subset=["selling_price"])

# ─── 3. Feature Engineering ─────────────────────────────────────────────────
curr_year = datetime.datetime.now().year

# Car age from year
df["car_age"] = curr_year - df["year"]

# Extract manufacturer from name
df["manufacturer"] = df["name"].str.split(" ").str[0]

# Drop columns we won't use
df = df.drop(["name", "year"], axis=1)

print(f"\n[2] After feature engineering → {df.shape[1]} columns")

# ─── 4. Handle Missing Values ───────────────────────────────────────────────
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols = [c for c in num_cols if c != "selling_price"]

for col in num_cols:
    df[col] = df[col].fillna(df[col].mean())

print("[3] Missing values handled")

# ─── 5. Train / Test Split ──────────────────────────────────────────────────
X = df.drop("selling_price", axis=1)
y = df["selling_price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ─── 6. One-Hot Encode Categoricals ─────────────────────────────────────────
cat_cols = ["manufacturer", "fuel", "seller_type", "transmission", "owner"]
cat_cols = [c for c in cat_cols if c in X_train.columns]

X_train = pd.get_dummies(X_train, columns=cat_cols, drop_first=True)
X_test  = pd.get_dummies(X_test,  columns=cat_cols, drop_first=True)

# Align columns (test may be missing some dummies)
missing_cols = set(X_train.columns) - set(X_test.columns)
for col in missing_cols:
    X_test[col] = 0
X_test = X_test[X_train.columns]

train_columns = X_train.columns.tolist()
print(f"[4] Encoded → {len(train_columns)} features")

# ─── 7. Scale ───────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ─── 8. Train All Three Models ──────────────────────────────────────────────
models = {
    "Linear Regression":       LinearRegression(),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
    "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
}

results = {}
print("\n[5] Training models …\n")
print(f"{'Model':<30} {'R² Score':>10} {'MAE':>12} {'RMSE':>12}")
print("-" * 65)

for name, model in models.items():
    model.fit(X_train_sc, y_train)
    y_pred = model.predict(X_test_sc)

    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    results[name] = {"r2": r2, "mae": mae, "rmse": rmse, "model": model}
    print(f"{name:<30} {r2:>10.4f} {mae:>12.2f} {rmse:>12.2f}")

best = max(results, key=lambda k: results[k]["r2"])
print(f"\n  Best model: {best}  (R² = {results[best]['r2']:.4f})")

# ─── 9. Save Models + Artifacts ─────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

for name, info in results.items():
    safe_name = name.lower().replace(" ", "_")
    path = os.path.join(MODELS_DIR, f"{safe_name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(info["model"], f)

with open(os.path.join(MODELS_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

with open(os.path.join(MODELS_DIR, "columns.pkl"), "wb") as f:
    pickle.dump(train_columns, f)

print("\n[6] Saved to /models/:")
for fname in os.listdir(MODELS_DIR):
    print(f"      {fname}")

# ─── 10. Comparison Bar Chart ───────────────────────────────────────────────
model_names  = list(results.keys())
r2_scores    = [results[m]["r2"] for m in model_names]

plt.figure(figsize=(9, 5))
bars = plt.bar(model_names, r2_scores, color=["#4A90D9", "#27AE60", "#E67E22"])
plt.ylim(0, 1)
plt.title("Model Comparison – R² Score", fontsize=14, fontweight="bold")
plt.ylabel("R² Score")
plt.xlabel("Model")
for bar, score in zip(bars, r2_scores):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.01,
             f"{score:.4f}", ha="center", va="bottom", fontsize=11)
plt.tight_layout()
chart_path = os.path.join(os.path.dirname(__file__), "static", "comparison.png")
plt.savefig(chart_path)
plt.close()
print(f"\n[7] Comparison chart saved → static/comparison.png")
print("\n✅ Training complete!\n")
