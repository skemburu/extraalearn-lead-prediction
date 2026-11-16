# ExtraaLearn Lead Conversion Prediction - Containerized Deployment

- `backend/` - Flask API (`GET /`, `POST /v1/predict`, `POST /v1/predictbatch`) serving the tuned Random Forest pipeline (`learn_model.joblib`) via Gunicorn on port 7860.
- `frontend/` - Streamlit UI (single + batch inference) on port 8501, calling the backend at `http://backend:7860` over the `learn-net` Docker network.
- `.devcontainer/` - Opening this repo in GitHub Codespaces builds and starts both containers automatically.
