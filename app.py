"""
AutoValuate - Flask Backend & Multi-Model Inference Engine
===========================================================
Architecture:
  - Session-based academic authentication
  - Multi-page routing:
      GET  /login     → User Authentication & Reviewer Access
      GET  /dashboard → Automotive Fleet Dashboard & Comparative Benchmark
      GET  /predict   → Interactive Valuation Studio
      POST /predict   → Tri-Model JSON Inference API
      GET  /logout    → Terminate Session
"""

import os
import pickle
import datetime

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "autovaluate-academic-capstone-key-2026")

# ─── Load Saved Machine Learning Artifacts ──────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

def load_pickle(filename):
    with open(os.path.join(MODELS_DIR, filename), "rb") as f:
        return pickle.load(f)

try:
    lr_model = load_pickle("linear_regression.pkl")
    rf_model = load_pickle("random_forest_regressor.pkl")
    dt_model = load_pickle("decision_tree_regressor.pkl")
    scaler   = load_pickle("scaler.pkl")
    columns  = load_pickle("columns.pkl")
    print("✅ All 3 ML models and preprocessing pipelines loaded successfully.")
except FileNotFoundError as e:
    print(f"⚠️ Model file missing: {e}. Run train_model.py first.")
    lr_model = rf_model = dt_model = scaler = columns = None

# Load exact manufacturer list directly from the training dataset
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "dataset.csv")
try:
    _df_dataset = pd.read_csv(DATA_FILE)
    MANUFACTURERS = sorted(_df_dataset["name"].str.split(" ").str[0].dropna().unique().tolist())
    print(f"✅ Loaded {len(MANUFACTURERS)} manufacturers directly from dataset.csv")
except Exception as e:
    print(f"⚠️ Could not read dataset.csv ({e}), falling back to trained columns.")
    MANUFACTURERS = sorted([c.replace("manufacturer_", "") for c in columns if c.startswith("manufacturer_")])


def build_input_df(form_data: dict) -> pd.DataFrame:
    """Transform user form inputs into the one-hot encoded and scaled feature vector."""
    curr_year = datetime.datetime.now().year

    car_age      = curr_year - int(form_data["year"])
    km_driven    = float(form_data["km_driven"])
    manufacturer = str(form_data["manufacturer"]).strip()
    fuel         = str(form_data["fuel"]).strip()
    seller_type  = str(form_data["seller_type"]).strip()
    transmission = str(form_data["transmission"]).strip()
    owner        = str(form_data["owner"]).strip()

    row = {col: 0 for col in columns}
    row["car_age"]   = car_age
    row["km_driven"] = km_driven

    # Manufacturer one-hot
    m_key = f"manufacturer_{manufacturer}"
    if m_key in row:
        row[m_key] = 1

    # Fuel one-hot
    f_key = f"fuel_{fuel}"
    if f_key in row:
        row[f_key] = 1

    # Seller Type one-hot
    s_key = f"seller_type_{seller_type}"
    if s_key in row:
        row[s_key] = 1

    # Transmission one-hot
    t_key = f"transmission_{transmission}"
    if t_key in row:
        row[t_key] = 1

    # Owner one-hot
    o_key = f"owner_{owner}"
    if o_key in row:
        row[o_key] = 1

    return pd.DataFrame([row])[columns]


# ─── Page Routes ────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Simple verification allowing academic demonstration access
        if username and password:
            # Extract display name
            display_name = username.split("@")[0].replace(".", " ").title()
            if not display_name:
                display_name = "Faculty Evaluator"
            session["user"] = display_name
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Please provide a valid username and password.")

    # If already logged in, redirect straight to dashboard
    if "user" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    # Ensure session or set default demo session
    if "user" not in session:
        session["user"] = "Faculty Reviewer"
    return render_template("dashboard.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    # POST handles AJAX prediction query
    if request.method == "POST":
        if any(m is None for m in [lr_model, rf_model, dt_model, scaler, columns]):
            return jsonify({"error": "ML Models not initialized. Run train_model.py first."}), 500

        try:
            data = request.get_json(force=True)
            df_input = build_input_df(data)
            scaled = scaler.transform(df_input)

            lr_pred = float(lr_model.predict(scaled)[0])
            rf_pred = float(rf_model.predict(scaled)[0])
            dt_pred = float(dt_model.predict(scaled)[0])

            def clean_price(val):
                return round(max(val, 15000), 2)

            return jsonify({
                "linear_regression": clean_price(lr_pred),
                "random_forest_regressor": clean_price(rf_pred),
                "decision_tree_regressor": clean_price(dt_pred),
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # GET renders the prediction studio page
    if "user" not in session:
        session["user"] = "Faculty Reviewer"
    return render_template("predict.html", manufacturers=MANUFACTURERS)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
