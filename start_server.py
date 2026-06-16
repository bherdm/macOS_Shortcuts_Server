import os
import subprocess
import sys
import shutil

# Configuration
# Using /opt/homebrew/bin/python3 as requested
PYTHON_BIN = "/opt/homebrew/bin/python3"
VENV_DIR = ".venv"
SERVER_CMD = "uvicorn macOS_shortcuts_server:app --host 0.0.0.0 --port 8012"
TMUX_SESSION = "mac_shortcuts"

def run_command(cmd, shell=True):
    """Helper to run shell commands."""
    try:
        # We use shell=True to allow 'source' and other shell builtins
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}")
        print(e)
        sys.exit(1)

def is_command_available(cmd):
    """Check if a command is available in the system PATH."""
    return shutil.which(cmd) is not None

def check_and_install_dependencies():
    """Checks for brew, python3, and tmux, installing them if necessary."""
    
    # 1. Check for Brew
    if not is_command_available("brew"):
        print("Error: 'brew' (Homebrew) is not installed.")
        print("Please install Homebrew from https://brew.sh/ first.")
        sys.exit(1)

    missing_deps = []

    # 2. Check for tmux
    if not is_command_available("tmux"):
        missing_deps.append("tmux")

    # 3. Check for python3 at the expected location
    if not os.path.exists(PYTHON_BIN):
        missing_deps.append("python3")

    if missing_deps:
        print(f"\n[!] Missing dependencies: {', '.join(missing_deps)}")
        user_choice = input(f"Do you want to install {', '.join(missing_deps)} using brew? (y/n): ").lower()
        
        if user_choice == 'y':
            print(f"[*] Installing {', '.join(missing_deps)}...")
            run_command(f"brew install {' '.join(missing_deps)}")
        else:
            print("Error: Missing dependencies required to run the server. Exiting.")
            sys.exit(1)

def main():
    # Prerequisite Check (Brew, Python, Tmux)
    check_and_install_dependencies()

    # 4. Handle Virtual Environment
    if not os.path.exists(VENV_DIR):
        print(f"[*] Creating virtual environment in {VENV_DIR}...")
        run_command(f"{PYTHON_BIN} -m venv {VENV_DIR}")
    else:
        print(f"[*] Virtual environment '{VENV_DIR}' already exists.")

    # 5. Ensure dependencies are installed in the venv (regardless of existence)
    pip_path = os.path.join(VENV_DIR, "bin", "pip")
    print("[*] Ensuring dependencies (fastapi) are installed in the venv...")
    run_command(f"{pip_path} install fastapi")

    # 6. Construct the command to run inside tmux
    # We source the venv to ensure 'uvicorn' is correctly resolved from the venv
    activate_script = os.path.join(VENV_DIR, "bin", "activate")
    tmux_command = f"source {activate_script} && {SERVER_CMD}"

    # 7. Start tmux session
    # First, kill any existing session with the same name to avoid conflicts
    if is_command_available("tmux"):
        subprocess.run(f"tmux kill-session -t {TMUX_SESSION} 2>/dev/null", shell=True, capture_output=True)

    print(f"[*] Starting tmux session: {TMUX_SESSION}")
    # -d starts it in detached mode so we can attach to it immediately
    run_command(f'tmux new-session -d -s {TMUX_SESSION} "{tmux_command}"')

    # 8. Enter the tmux session
    print(f"[!] Attached to tmux session '{TMUX_SESSION}'.")
    print("[!] To 'escape' and leave the server running, press: Ctrl+b then d")
    print("-" * 60)
    
    run_command(f"tmux attach-session -t {TMUX_SESSION}")

    print("-" * 60)
    print(f"[+] Server is still running in the background in tmux session '{TMUX_SESSION}'.")
    print(f"[+] To re-attach later, run: tmux attach-session -t {TMUX_SESSION}")

if __name__ == "__main__":
    main()