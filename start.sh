#!/bin/bash

# Start the Fast API backend in the background
# We bind to 0.0.0.0 to be safe, though 127.0.0.1 is fine for internal comms
python -m uvicorn backend:app --host 127.0.0.1 --port 8000 &

# Start the Streamlit frontend in the foreground
# Render provides the port in the $PORT environment variable
echo "Starting Streamlit on port $PORT"
python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0
