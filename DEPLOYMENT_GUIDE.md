# 🚀 Deployment Guide: Car Resale Price Prediction

This guide provides clear, step-by-step instructions to deploy your Machine Learning project to the cloud so anyone (including your teacher) can access it through a public URL.

---

## 🎯 Which Platform Should You Choose?

| Platform | Best For | Cost | Difficulty | Verdict |
|---|---|---|---|---|
| **Streamlit Community Cloud** | Machine Learning Apps (`streamlit_app.py`) | **100% Free** | ⭐ Very Easy (2 mins) | **RECOMMENDED** — Native Python ML hosting, no credit card required. |
| **Render.com** | Flask Web App (`app.py`) | **100% Free** | ⭐⭐ Easy (3 mins) | Best if you want the exact Flask HTML/CSS interface live. |
| **Firebase** | Static websites & Mobile apps | Free tier | ⭐⭐⭐⭐ Complex | Requires Google Cloud Run + Docker because Firebase alone does not run Python. |

---

## 🌟 Method 1: Deploy on Streamlit Cloud (Recommended & Easiest)

Streamlit Community Cloud is the industry-standard way to deploy Python machine learning models directly from GitHub for free.

### Step 1: Test the Streamlit App Locally First
Open your Terminal and run:
```bash
cd /Users/SujalSingh/Machine_Learnig_1
python3 -m streamlit run streamlit_app.py
```
This will open `http://localhost:8501` in your browser. Verify that the Dashboard, Prediction form, and Login work cleanly. Press `Ctrl + C` in Terminal when done.

---

### Step 2: Push Your Project to GitHub
If you haven't put your project on GitHub yet, run these commands in your Terminal:

1. **Initialize Git & Commit:**
   ```bash
   cd /Users/SujalSingh/Machine_Learnig_1
   git init
   git add .
   git commit -m "Complete Car Resale Prediction Project with 3 ML models"
   ```

2. **Create a GitHub Repository:**
   - Go to [github.com](https://github.com) and log in.
   - Click the **"+"** icon in the top right &rarr; **New repository**.
   - Name it `car-resale-price-prediction`.
   - Keep it **Public** (required for free Streamlit deployment).
   - Do **NOT** check "Initialize with README" (we already have our files).
   - Click **Create repository**.

3. **Push your code:**
   Copy and run the 3 commands GitHub shows you:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/car-resale-price-prediction.git
   git push -u origin main
   ```

---

### Step 3: Deploy on Streamlit Community Cloud (Takes 60 seconds)
1. Go to **[share.streamlit.io](https://share.streamlit.io)**.
2. Click **"Continue with GitHub"** and log in.
3. Click the blue **"Create app"** button.
4. Fill in the three fields:
   - **Repository:** `YOUR_USERNAME/car-resale-price-prediction`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **"Deploy!"**

Streamlit will install your dependencies from `requirements.txt`, load your saved models from `models/`, and give you a public URL like:
👉 `https://car-resale-prediction-xyz.streamlit.app`

---

## 🌐 Method 2: Deploy the Flask App on Render.com (100% Free)

If you prefer to deploy the custom HTML/CSS Flask web interface (`app.py`), **Render.com** is the best free host.

### Step 1: Add `gunicorn` to `requirements.txt`
In `requirements.txt`, make sure `gunicorn` is listed (for production server):
```
flask>=2.3.0
gunicorn>=21.2.0
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
```

### Step 2: Deploy on Render
1. Go to **[render.com](https://render.com)** and sign up for a free account (sign in with GitHub).
2. On your dashboard, click **"New +"** &rarr; **"Web Service"**.
3. Select **"Build and deploy from a Git repository"** and choose your `car-resale-price-prediction` repository.
4. Configure the settings:
   - **Name:** `car-resale-predictor`
   - **Language:** `Python 3`
   - **Region:** Any (e.g., Oregon or Frankfurt)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`
5. Click **"Create Web Service"**.

Render will build the app and give you a live URL like:
👉 `https://car-resale-predictor.onrender.com`

---

## ☁️ Method 3: Can We Deploy on Firebase?

### Important Note about Firebase:
**Firebase Hosting** is designed exclusively for **static frontend files** (HTML, CSS, JavaScript) or **Node.js** cloud functions. 

Because our application runs **Python with Scikit-learn machine learning binaries** (`.pkl` files), Firebase cannot execute Python scripts directly on its standard free hosting.

To run Python on Firebase, Google requires:
1. Docker containerizing the Flask app (`Dockerfile`).
2. Deploying the container to **Google Cloud Run**.
3. Rewriting Firebase Hosting routes to the Cloud Run service.
4. This requires an active Google Cloud Platform (GCP) account with credit card billing enabled.

> **Recommendation for College/Viva:**  
> Use **Streamlit Cloud** (Method 1) or **Render** (Method 2). Both are 100% free, require zero credit cards, and run in 2 minutes.

---

## ✅ How to Verify and Check the Working of the Deployed App

Once your app is deployed online, test these 4 checks to ensure everything works smoothly:

### 1. Verification Checklist

| Test Case | How to Test | Expected Result |
|---|---|---|
| **1. UI Load Test** | Open the live URL on your computer and phone. | Page loads cleanly with navigation and table. |
| **2. Dashboard Metrics** | Check the benchmark table on `/dashboard`. | Shows Linear Regression (57.7%), Decision Tree (67.7%), Random Forest (71.6%). |
| **3. Brand Logo Cards** | Check the 4 brand cards. | Shows Maruti Suzuki, Honda, Hyundai, and Toyota with classic logos. |
| **4. Prediction Execution** | Fill form with: Maruti, 2017, 65,000 km, Diesel, Manual, First Owner &rarr; Click **Predict**. | Returns 3 prices (Linear: ~₹ 4.8L, Decision Tree: ~₹ 4.75L, Random Forest: ~₹ 4.85L). |
| **5. Model Recommendation** | Verify the results card. | Random Forest is clearly highlighted as the **Best Model**. |

---

## 📌 Summary Commands Cheatsheet

```bash
# 1. Test Flask locally:
python3 app.py

# 2. Test Streamlit locally:
python3 -m streamlit run streamlit_app.py

# 3. Push updates to GitHub:
git add .
git commit -m "Update project"
git push origin main
```
