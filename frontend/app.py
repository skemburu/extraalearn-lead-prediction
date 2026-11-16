import os
import pandas as pd
import requests
import streamlit as st

# Base URL of the Flask backend (Docker network container name "backend")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860")

st.set_page_config(page_title="ExtraaLearn Lead Prediction", layout="centered")
st.title("Lead Prediction System")
st.write("Enter the lead details below to predict whether the lead will convert to a paid customer.")

tab_single, tab_batch = st.tabs(["Single Inference", "Batch Inference"])

with tab_single:
    age = st.number_input("Age", min_value=0, value=25)
    current_occupation = st.selectbox("Current Occupation", ["Professional", "Unemployed", "Student"])
    first_interaction = st.selectbox("First Interaction Platform", ["Website", "Mobile App"])
    profile_completed = st.selectbox("Profile Completion Level", ["Low", "Medium", "High"])
    website_visits = st.number_input("Number of Website Visits", min_value=0, value=3)
    time_spent_on_website = st.number_input("Time Spent on Website (in seconds)", min_value=0.0, value=180.0)
    page_views_per_visit = st.number_input("Page Views per Visit", min_value=0.0, value=4.5)
    last_activity = st.selectbox("Last Activity Type", ["Email Activity", "Phone Activity", "Website Activity"])
    print_media_type1 = st.selectbox("Seen Newspaper Ad?", ["Yes", "No"], index=1)
    print_media_type2 = st.selectbox("Seen Magazine Ad?", ["Yes", "No"], index=1)
    digital_media = st.selectbox("Seen Digital Media Ad?", ["Yes", "No"], index=1)
    educational_channels = st.selectbox("Heard via Educational Channels?", ["Yes", "No"], index=1)
    referral = st.selectbox("Heard via Referral?", ["Yes", "No"], index=1)

    lead_data = {
        "age": age, "current_occupation": current_occupation, "first_interaction": first_interaction,
        "profile_completed": profile_completed, "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website, "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity, "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2, "digital_media": digital_media,
        "educational_channels": educational_channels, "referral": referral,
    }

    if st.button("Predict", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=lead_data)
        if response.status_code == 200:
            result = response.json()
            label = "Will convert" if result["Lead"] == 1 else "Will not convert"
            st.success(f"Predicted Lead Conversion: {result['Lead']} ({label})")
            st.write(f"Conversion probability: {result['conversion_probability']:.1%}")
            st.json(result)
        else:
            st.error("Unable to connect to the prediction API.")

with tab_batch:
    st.write("Upload a CSV file with the 13 lead attributes (an optional ID column is passed through).")
    uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])
    if uploaded_file is not None and st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch",
                                 files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")})
        if response.status_code == 200:
            results = pd.DataFrame(response.json())
            st.success(f"Batch predictions completed for {len(results)} leads "
                       f"({int(results['Lead'].sum())} predicted to convert).")
            st.dataframe(results, use_container_width=True)
            st.download_button("Download predictions", results.to_csv(index=False), "batch_predictions.csv")
        else:
            st.error("Unable to connect to the prediction API.")
