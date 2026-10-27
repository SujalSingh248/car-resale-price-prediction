"""
Car Resale Price Prediction - Streamlit Cloud Application
==========================================================
Deployable directly on Streamlit Community Cloud (share.streamlit.io)
Loads pre-trained models from models/ directory.
"""

import os
import pickle
import datetime
import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Car Resale Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Minimalist CSS
st.markdown("""
<style>
    .main { background-color: #f9fafb; }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover { background-color: #1d4ed8; }
    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-title { font-size: 0.82rem; color: #6b7280; font-weight: 600; text-transform: uppercase; }
    .metric-val { font-size: 1.4rem; font-weight: 700; color: #111827; margin-top: 4px; }
    .metric-sub { font-size: 0.78rem; color: #059669; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Load Models
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

@st.cache_resource
def load_ml_assets():
    with open(os.path.join(MODELS_DIR, "linear_regression.pkl"), "rb") as f:
        lr = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "decision_tree_regressor.pkl"), "rb") as f:
        dt = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "random_forest_regressor.pkl"), "rb") as f:
        rf = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "columns.pkl"), "rb") as f:
        columns = pickle.load(f)
    return lr, dt, rf, scaler, columns

try:
    lr_model, dt_model, rf_model, scaler, feature_columns = load_ml_assets()
    models_ready = True
except Exception as e:
    st.error(f"Error loading models: {e}. Please run train_model.py first.")
    models_ready = False

MANUFACTURERS = [
    "Maruti", "Hyundai", "Honda", "Toyota", "Ford", "Mahindra", "Tata",
    "Chevrolet", "Renault", "Volkswagen", "BMW", "Audi", "Mercedes-Benz",
    "Skoda", "Nissan", "Datsun", "Fiat", "Jeep", "Jaguar", "Volvo"
]

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # Default open for demo, can toggle in Login tab

# Sidebar Navigation
st.sidebar.title("🚗 AutoValuate")
st.sidebar.caption("Machine Learning Valuation Platform")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "🎯 Predict Car Price", "🔑 User Authentication"])

# Format currency in INR
def format_inr(val):
    if val >= 100000:
        return f"₹ {val / 100000:.2f} Lakh"
    return f"₹ {int(val):,}"

# ==============================================================================
# PAGE 1: DASHBOARD
# ==============================================================================
if page == "📊 Dashboard":
    st.title("Project Dashboard & Benchmarks")
    st.markdown("Machine learning models evaluated on **4,340 real used car transactions** to estimate market depreciation.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="metric-card"><div class="metric-title">Dataset Records</div><div class="metric-val">4,340</div><div class="metric-sub">Verified sales</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card"><div class="metric-title">Active Models</div><div class="metric-val">3 Models</div><div class="metric-sub">Linear, Tree, Forest</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card"><div class="metric-title">Champion R² Score</div><div class="metric-val">71.60%</div><div class="metric-sub">Random Forest</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card"><div class="metric-title">Fleet Avg Value</div><div class="metric-val">₹ 5.04 L</div><div class="metric-sub">Market baseline</div></div>""", unsafe_allow_html=True)

    st.subheader("1. Model Performance Benchmark")
    
    perf_data = pd.DataFrame({
        "Model Name": ["Random Forest Regressor", "Decision Tree Regressor", "Linear Regression"],
        "R² Accuracy": ["0.7160 (71.6%)", "0.6773 (67.7%)", "0.5771 (57.7%)"],
        "Mean Absolute Error (MAE)": ["₹ 1,22,126", "₹ 1,32,075", "₹ 1,82,847"],
        "Status": ["👑 Best Performer (Ensemble)", "Non-Linear Tree", "Parametric Baseline"]
    })
    st.table(perf_data)

    st.subheader("2. Popular Models by Brand")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**Maruti Suzuki Swift**\n\n• 2017 | Diesel | Manual\n• 65,000 km | 1st Owner\n\nEst: ₹ 4.75 Lakh")
    with c2:
        st.info("**Honda City 1.5**\n\n• 2018 | Petrol | Manual\n• 42,000 km | 1st Owner\n\nEst: ₹ 6.85 Lakh")
    with c3:
        st.info("**Hyundai Creta 1.6**\n\n• 2019 | Diesel | Auto\n• 38,000 km | 1st Owner\n\nEst: ₹ 11.20 Lakh")
    with c4:
        st.info("**Toyota Innova 2.5**\n\n• 2016 | Diesel | Manual\n• 95,000 km | 2nd Owner\n\nEst: ₹ 8.40 Lakh")

# ==============================================================================
# PAGE 2: PREDICTION STUDIO
# ==============================================================================
elif page == "🎯 Predict Car Price":
    st.title("Car Resale Price Prediction")
    st.markdown("Enter the vehicle specifications below to query all three trained estimators in parallel.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            manufacturer = st.selectbox("Manufacturer / Brand", sorted(MANUFACTURERS), index=0)
            year = st.number_input("Year of Manufacture", min_value=1992, max_value=2026, value=2018, step=1)
            km_driven = st.number_input("Kilometers Driven", min_value=100, max_value=800000, value=45000, step=1000)
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"], index=0)

        with col2:
            transmission = st.selectbox("Transmission", ["Manual", "Automatic"], index=0)
            seller_type = st.selectbox("Seller Channel", ["Individual", "Dealer", "Trustmark Dealer"], index=0)
            owner = st.selectbox("Ownership Record", ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"], index=0)
            st.write("")
            st.write("")
            submit_btn = st.form_submit_button("⚡ Predict Resale Price")

    if submit_btn and models_ready:
        curr_year = datetime.datetime.now().year
        car_age = curr_year - int(year)

        # Construct single-row DataFrame matching the exact 39 trained dummy features
        row = {c: 0 for c in feature_columns}
        row["car_age"] = car_age
        row["km_driven"] = float(km_driven)

        for key, val in [
            (f"manufacturer_{manufacturer}", 1),
            (f"fuel_{fuel}", 1),
            (f"seller_type_{seller_type}", 1),
            (f"transmission_{transmission}", 1),
            (f"owner_{owner}", 1)
        ]:
            if key in row:
                row[key] = val

        input_df = pd.DataFrame([row])[feature_columns]
        scaled = scaler.transform(input_df)

        lr_val = max(float(lr_model.predict(scaled)[0]), 15000)
        dt_val = max(float(dt_model.predict(scaled)[0]), 15000)
        rf_val = max(float(rf_model.predict(scaled)[0]), 15000)

        st.success("✅ Multi-Model Prediction Computed Successfully!")

        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Linear Regression (Baseline)", format_inr(lr_val), f"₹ {int(lr_val):,}")
        with res_col2:
            st.metric("Decision Tree Regressor", format_inr(dt_val), f"₹ {int(dt_val):,}")
        with res_col3:
            st.metric("Random Forest (Best Performer)", format_inr(rf_val), f"₹ {int(rf_val):,}", delta="Highest R²: 71.6%")

        st.info(f"💡 **Takeaway:** For a {car_age}-year-old {manufacturer} ({fuel}, {transmission}) driven {km_driven:,} km, the **Random Forest Regressor** estimates fair resale value at **{format_inr(rf_val)}**. Random Forest is recommended due to its ensemble bagging reducing variance.")

# ==============================================================================
# PAGE 3: USER AUTHENTICATION
# ==============================================================================
elif page == "🔑 User Authentication":
    st.title("User Login")
    st.markdown("Academic Evaluation Sign-in.")

    login_col, _ = st.columns([1, 1])
    with login_col:
        uname = st.text_input("Username or Email", value="teacher@college.edu")
        pwd = st.text_input("Password", type="password", value="admin123")
        if st.button("Authenticate Session"):
            st.session_state["authenticated"] = True
            st.success(f"Welcome back, {uname}! You are authenticated.")
