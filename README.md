# Deepfake Detector — Runnable Starter

This starter contains a Flask backend wired to a tiny toy classifier wrapper (PyTorch optional).

Quick start (local):

1. Create a Python virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. (Optional) Install torch & torchvision if you want model behavior: `pip install torch torchvision`
4. Run the Flask app: `python backend/app.py`
5. Open http://localhost:5000/ and login with `test@example.com` / `password123`

Notes:
- The toy model is a deterministic stub if PyTorch isn't installed.
- Replace the toy model with a trained model for real detection.
