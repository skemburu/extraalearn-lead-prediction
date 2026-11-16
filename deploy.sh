#!/usr/bin/env bash
# Build and run the Flask backend and Streamlit frontend as separate Docker containers
# on a shared Docker network, then make the forwarded ports public.
set -x
cd "$(dirname "$0")"
docker network create learn-net || true
docker build -t learn-backend ./backend
docker build -t learn-frontend ./frontend
docker rm -f backend frontend || true
docker run -d --name backend --network learn-net -p 7860:7860 learn-backend
docker run -d --name frontend --network learn-net -p 8501:8501 learn-frontend
for i in $(seq 1 30); do curl -sf http://localhost:7860/ >/dev/null && curl -sf http://localhost:8501/ >/dev/null && break; sleep 3; done
gh codespace ports visibility 7860:public 8501:public -c "$CODESPACE_NAME"
docker ps
echo "Backend:  https://${CODESPACE_NAME}-7860.app.github.dev"
echo "Frontend: https://${CODESPACE_NAME}-8501.app.github.dev"
