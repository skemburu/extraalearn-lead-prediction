# Import necessary libraries
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
learn_api = Flask("ExtraaLearn")

# Load the trained lead conversion prediction model (full preprocessing + tuned Random Forest pipeline)
model = joblib.load("learn_model.joblib")

FEATURES = ['age', 'current_occupation', 'first_interaction', 'profile_completed',
            'website_visits', 'time_spent_on_website', 'page_views_per_visit',
            'last_activity', 'print_media_type1', 'print_media_type2',
            'digital_media', 'educational_channels', 'referral']

# Define a route for the home page
@learn_api.get('/')
def home():
    return "Welcome to the Lead Prediction System"

# Endpoint to predict conversion for a single lead
@learn_api.post('/v1/predict')
def predict_lead():
    data = request.get_json()
    sample = {f: data[f] for f in FEATURES}
    input_data = pd.DataFrame([sample])
    prediction = int(model.predict(input_data)[0])
    probability = float(model.predict_proba(input_data)[0, 1])
    return jsonify({'Lead': prediction, 'conversion_probability': round(probability, 4)})

# Endpoint to predict conversion for a batch of leads uploaded as a CSV file
@learn_api.post('/v1/predictbatch')
def predict_lead_batch():
    file = request.files['file']
    input_data = pd.read_csv(file)
    preds = model.predict(input_data[FEATURES]).tolist()
    probs = model.predict_proba(input_data[FEATURES])[:, 1].round(4).tolist()
    ids = input_data['ID'].tolist() if 'ID' in input_data.columns else list(range(1, len(input_data) + 1))
    return jsonify([{'ID': i, 'Lead': int(p), 'conversion_probability': float(q)} for i, p, q in zip(ids, preds, probs)])

# Run the Flask app in debug mode
if __name__ == '__main__':
    learn_api.run(debug=True)
