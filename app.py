import streamlit as st
import pandas as pd
import joblib

# Load both models from the saved file
artifact = joblib.load("cyber_threat_classifier.joblib")

attack_model = artifact["attack_model"]
attack_scaler = artifact["attack_scaler"]
target_encoder = artifact["target_encoder"]
attack_features = artifact["attack_features"]

severity_model = artifact["severity_model"]
severity_scaler = artifact["severity_scaler"]
severity_features = artifact["severity_features"]

st.set_page_config(page_title="SOC Threat & Triage Dashboard", layout="centered")
st.title("Cybersecurity Threat & Triage Dashboard")
st.write("Enter incident details below to identify the attack type and determine urgency level.")

# User input form
with st.form("incident_form"):
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Year", min_value=2015, max_value=2030, value=2024)
        country = st.selectbox("Country", ["USA", "UK", "Germany", "France", "India", "China", "Japan", "Brazil", "Russia", "Australia"])
        industry = st.selectbox("Target Industry", ["Banking", "Healthcare", "IT", "Retail", "Government", "Education", "Telecommunications"])
        loss = st.number_input("Financial Loss (in Million $)", min_value=0.0, value=25.0, step=0.5)
    with col2:
        users = st.number_input("Number of Affected Users", min_value=1, value=50000, step=1000)
        res_time = st.number_input("Incident Resolution Time (Hours)", min_value=1, value=24)
        source = st.selectbox("Attack Source", ["Hacker Group", "Nation-state", "Insider", "Unknown"])
        vuln = st.selectbox("Security Vulnerability Type", ["Zero-day", "Phishing", "Unpatched Software", "Weak Passwords", "Social Engineering"])
        defense = st.selectbox("Defense Mechanism Used", ["Firewall", "VPN", "Antivirus", "Encryption", "AI-based Detection"])

    submitted = st.form_submit_button("Analyze Incident")

if submitted:
    # Build base row from user inputs
    base_data = {
        "Country": country,
        "Year": year,
        "Target Industry": industry,
        "Financial Loss (in Million $)": loss,
        "Number of Affected Users": users,
        "Attack Source": source,
        "Security Vulnerability Type": vuln,
        "Defense Mechanism Used": defense,
        "Incident Resolution Time (Hours)": res_time
    }

    # --- PREDICTION 1: ATTACK TYPE ---
    df_attack = pd.DataFrame([base_data])
    df_attack["Loss_Per_User"] = (df_attack["Financial Loss (in Million $)"] * 1_000_000) / (df_attack["Number of Affected Users"] + 1)
    df_attack["Loss_Per_Hour"] = df_attack["Financial Loss (in Million $)"] / (df_attack["Incident Resolution Time (Hours)"] + 1)

    aligned_attack = pd.get_dummies(df_attack).reindex(columns=attack_features, fill_value=0)
    scaled_attack = attack_scaler.transform(aligned_attack)
    pred_attack_idx = attack_model.predict(scaled_attack)[0]
    pred_attack_label = target_encoder.inverse_transform([pred_attack_idx])[0]

    # --- PREDICTION 2: SEVERITY TRIAGE (Uses predicted Attack Type as an input!) ---
    sev_data = base_data.copy()
    sev_data["Attack Type"] = pred_attack_label
    df_sev = pd.DataFrame([sev_data])

    aligned_sev = pd.get_dummies(df_sev).reindex(columns=severity_features, fill_value=0)
    scaled_sev = severity_scaler.transform(aligned_sev)
    pred_sev = severity_model.predict(scaled_sev)[0]

    # --- DISPLAY BOTH RESULTS SIDE BY SIDE ---
    st.divider()
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.subheader("1. Attack Classification")
        st.info(f"**Detected Vector:** {pred_attack_label}")

    with res_col2:
        st.subheader("2. SOC Priority Level")
        if pred_sev == 1:
            st.error("**CRITICAL (Tier-3 Escalation)**")
        else:
            st.success("**STANDARD (Routine Handling)**")

    # Confidence chart for Attack Type
    if hasattr(attack_model, "predict_proba"):
        st.write("**Attack Type Probability Breakdown:**")
        probs = attack_model.predict_proba(scaled_attack)[0]
        prob_df = pd.DataFrame({"Attack Type": target_encoder.classes_, "Confidence (%)": (probs * 100).round(2)})
        
        st.bar_chart(prob_df.set_index("Attack Type"))