import os
import sys

# Add the backend directory to the search path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the FastAPI app from backend/main.py
try:
    from main import app
except Exception as e:
    # Diagnostic fallback for Test 1 tracking
    from fastapi import FastAPI
    import traceback
    app = FastAPI(title="Primers Diagnostic")
    
    @app.get("/api")
    def root():
        return {
            "status": "IMPORT_FAILED",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "python": sys.version,
            "cwd": os.getcwd(),
            "backend_exists": os.path.exists(backend_path)
        }
