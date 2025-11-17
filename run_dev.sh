#!/usr/bin/env bash
# helper for unix/mac - run backend and serve frontend
cd backend
uvicorn main:app --reload &
SERVER_PID=$!
cd ../frontend
python -m http.server 3000 &
wait $SERVER_PID
