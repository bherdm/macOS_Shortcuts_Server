# macOS_shortcuts_server.py
"""
macOS Shortcuts API — Triggers macOS Shortcuts via HTTP.

Run with:
uvicorn macOS_shortcuts_server:app --host 0.0.0.0 --port 8012
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess

# --- Models ---

class ShortcutRequest(BaseModel):
    name: str

class ShortcutResponse(BaseModel):
    shortcut_name: str
    output: Optional[str] = None
    error: Optional[str] = None

# --- Shortcut Logic ---

def run_mac_shortcut(shortcut_name):
    """Runs the macOS shortcut and returns the output as a string."""
    try:
        result = subprocess.check_output(['shortcuts', 'run', shortcut_name], stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing shortcut: {e.output}")
        return None
    except FileNotFoundError:
        print("The 'shortcuts' command was not found. Make sure you are running this on macOS.")
        return None


# --- API App ---

app = FastAPI(
    title="macOS Shortcuts API",
    description="An API to trigger macOS Shortcuts remotely.",
    version="1.0.0"
)

@app.post("/run", response_model=ShortcutResponse)
async def run_shortcut(request: ShortcutRequest):
    """
    Triggers the specified macOS Shortcut by name.
    
    **Request Body:**
    - `name`: The exact name of the shortcut as it appears in the Shortcuts app.
    """
    result = run_mac_shortcut(request.name)
    
    if result is None:
        # The manager function prints the error to console, 
        # so we return a generic error to the API caller.
        return ShortcutResponse(
            shortcut_name=request.name,
            error="Execution failed. Check server logs for details."
        )
    
    return ShortcutResponse(
        shortcut_name=request.name,
        output=result
    )

@app.get("/health")
async def health():
    """Returns system health status."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # Note: Using the filename as the application module
    uvicorn.run(app, host="0.0.0.0", port=8012)