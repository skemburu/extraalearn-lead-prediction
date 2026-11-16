#!/usr/bin/env bash
# Build and run the Flask backend and Streamlit frontend as separate Docker containers
# connected through a user-defined Docker network.
set -x
cd "$(dirname "$0")/.."
docker network create learn-net || true
docker build -t learn-backend ./backend
docker build -t learn-frontend ./frontend
docker rm -f backend frontend || true
docker run -d --name backend --network learn-net -p 7860:7860 learn-backend
docker run -d --name frontend --network learn-net -p 8501:8501 learn-frontend
sleep 10
# Make the forwarded ports public so the API and UI can be reached without GitHub sign-in
gh codespace ports visibility 7860:public 8501:public -c "$CODESPACE_NAME" || true
docker ps
