#!/bin/bash

# Start the FastAPI backend
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
sleep 5

# Start the Streamlit frontend
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0