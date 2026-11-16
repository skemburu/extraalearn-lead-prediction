#!/usr/bin/env bash
# Wait for both containers to be serving, then make the forwarded ports public.
for i in $(seq 1 60); do
  curl -sf http://localhost:7860/ >/dev/null && curl -sf http://localhost:8501/ >/dev/null && break
  sleep 5
done
for i in $(seq 1 12); do
  gh codespace ports visibility 7860:public 8501:public -c "$CODESPACE_NAME" && break
  sleep 10
done
