# macOS Shortcuts Server

An API server that allows you to trigger macOS Shortcuts remotely via HTTP requests.

This project provides a lightweight FastAPI server that listens for incoming POST requests and executes the corresponding macOS Shortcut using the system's shell. It is designed to act as a bridge between external devices/services and your local macOS automation workflows.

## 🚀 Features

- **Remote Execution**: Trigger any macOS Shortcut by name via a simple REST API.
- **Response Capture**: Receives the output of the shortcut and returns it in the HTTP response.
- **Background Operation**: Includes a startup script that manages a Python virtual environment and runs the server in a `tmux` session for easy background management.
- **Automated Setup**: Automatically checks for and installs required system dependencies (`tmux`, `python3`) using Homebrew.
- **Health Checks**: Built-in `/health` endpoint for monitoring server status.

## 🛠 Prerequisites

- **macOS**: Required (to access the macOS Shortcuts app).
- **Homebrew**: Required for automated dependency installation.
- **Python 3 & tmux**: Handled automatically by the startup script.

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd macos-shortcuts-server
   ```

2. **Run the startup script:**
   The included `start_server.py` script automates the setup process. It:
   - Checks for system dependencies (`tmux`, `python3`) and installs them via `brew` if they are missing.
   - Creates a Python virtual environment.
   - Installs required Python dependencies (`fastapi`).
   - Launches the server inside a `tmux` session.

   ```bash
   python3 start_server.py
   ```

   *Note: The startup script expects Python to be located at `/opt/homebrew/bin/python3` by default. If your Python path is different, please edit `start_server.py` accordingly.*

## 🚀 Usage

### API Endpoints

#### 1. Run a Shortcut
Executes the specified shortcut.

- **URL:** `/run`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "name": "Your Shortcut Name"
  }
  ```
- **Success Response:**
  ```json
  {
    "shortcut_name": "Your Shortcut Name",
    "output": "The result from the shortcut",
    "error": null
  }
  ```
- **Error Response:**
  ```json
  {
    "shortcut_name": "Your Shortcut Name",
    "output": null,
    "error": "Execution failed. Check server logs for details."
  }
  ```

#### 2. Health Check
Checks if the server is running.

- **URL:** `/health`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "status": "ok"
  }
  ```

### Managing the Server

The server runs inside a `tmux` session named `mac_shortcuts`.

- **To view server logs:** 
  ```bash
  tmux attach-session -t mac_shortcuts
  ```
- **To detach from the session (keep server running):** 
  Press `Ctrl+b` then `d`.

## ⚠️ Disclaimer

This tool executes shell commands on your macOS system. Ensure you only run shortcuts that you trust and use this server in a secure network environment.