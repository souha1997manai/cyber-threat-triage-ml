# cyber-threat-triage-ml
# 🛡️ Cybersecurity Threat & SOC Triage Dashboard

An end-to-end Machine Learning and Security Operations Center (SOC) triage web application built to classify cyber attack vectors and automate incident escalation priority from global threat telemetry (2015–2024).

🔗 **Live Interactive App:** [Launch Dashboard on Streamlit](https://cyber-threat-triage-ml-9xvoyhaf64tczagakxhfnl.streamlit.app)

---

## 📌 Project Overview

Security Operations Centers face high alert volumes and must rapidly determine both **what type of attack** is occurring and **how urgently** it requires Tier-3 incident response. Using a dataset of 3,000 global cybersecurity incidents, this project implements a leakage-free preprocessing pipeline, domain-specific feature engineering, and a dual-model inference engine deployed as an interactive Streamlit dashboard.

---

## 🧠 Dual-Model Architecture

The deployed artifact (`cyber_threat_classifier.joblib`) bundles two independent classification pipelines and their fitted `StandardScaler` and schema alignment encoders:

1. **Experiment 1 — Attack Vector Classification**
   * **Objective:** Predict the probable cyber attack category (e.g., Ransomware, Phishing, DDoS, Malware, Man-in-the-Middle, SQL Injection) from incident metadata.
   * **Feature Engineering:** Incorporates financial impact velocity and per-capita severity ratios (`Loss_Per_User` and `Loss_Per_Hour`) alongside one-hot encoded categorical telemetry.
   * **Output:** Predicted attack class and full probability distribution across all threat vectors.

2. **Experiment 2 — Automated SOC Severity Triage**
   * **Objective:** Classify incoming incidents into **Standard (0)** routine handling vs. **Critical (1)** Tier-3 escalation.
   * **Leakage Prevention:** Excludes post-incident outcome metrics (financial loss and resolution time) during training so predictions reflect real-time triage conditions.

---

## 📊 Dataset Summary

* **Source:** Global Cybersecurity Threats Dataset (2015–2024)
* **Volume:** 3,000 incident records across 10 core attributes (0 missing values, 0 duplicates)
* **Features:** `Country`, `Year`, `Attack Type`, `Target Industry`, `Financial Loss (in Million $)`, `Number of Affected Users`, `Attack Source`, `Security Vulnerability Type`, `Defense Mechanism Used`, and `Incident Resolution Time (Hours)`.

---

## 📂 Repository Structure

```text
cyber-threat-triage-ml/
├── app.py                                      # Streamlit web application & inference UI
├── cyber_threat_classifier.joblib              # Compressed dual-model artifact & scalers
├── Global_Cybersecurity_Threats_2015-2024.csv  # Raw incident dataset (3,000 records)
├── Untitled.ipynb                              # Full EDA, feature engineering & model training notebook
├── requirements.txt                            # Python dependencies for cloud deployment
└── README.md                                   # Project documentation

## 💻 Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/souha1997manai/cyber-threat-triage-ml.git
   cd cyber-threat-triage-ml
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Tech Stack

* **Language:** Python
* **Machine Learning & Data:** Scikit-Learn, Pandas, NumPy, Joblib
* **Visualization & Deployment:** Matplotlib, Seaborn, Streamlit Community Cloud
