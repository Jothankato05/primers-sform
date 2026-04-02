import os
import sys
import traceback

# List the current directory to see what Vercel has mounted
root_files = os.listdir(".") if os.path.exists(".") else []
cwd = os.getcwd()

# Add the backend directory to the search path
# We check multiple potential locations
backend_locations = [
    os.path.join(os.path.dirname(__file__), "..", "backend"),
    os.path.join(os.getcwd(), "backend"),
    "/var/task/backend"
]

backend_path = None
for loc in backend_locations:
    if os.path.exists(loc):
        backend_path = loc
        if loc not in sys.path:
            sys.path.insert(0, loc)
        break

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def diagnostic_root():
    try:
        from main import app as main_app
        return {
            "status": "BRIDGE_SUCCESS",
            "cwd": cwd,
            "root_files": root_files,
            "backend_path": backend_path,
            "main_imported": True
        }
    except Exception as e:
        return {
            "status": "IMPORT_FAILED",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "cwd": cwd,
            "backend_locations": backend_locations,
            "path": sys.path
        }

@app.get("/api")
def api_root():
    return diagnostic_root()
