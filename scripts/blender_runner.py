"""
Blender 5.1 Headless Execution Bridge
Executes Python automation scripts inside Blender 5.1.
Usage:
    python scripts/blender_runner.py path/to/script.py [optional arguments]
"""

import sys
import subprocess
import os
from pathlib import Path

BLENDER_EXE = r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

def run_blender_script(script_path: str, extra_args: list = None):
    if not os.path.exists(BLENDER_EXE):
        raise FileNotFoundError(f"Blender executable not found at: {BLENDER_EXE}")
    
    script_file = Path(script_path).resolve()
    if not script_file.exists():
        raise FileNotFoundError(f"Script file not found at: {script_file}")

    cmd = [
        BLENDER_EXE,
        "--background",
        "--factory-startup",
        "--python", str(script_file)
    ]
    
    if extra_args:
        cmd.append("--")
        cmd.extend(extra_args)

    print(f"[*] Executing Blender 5.1 with script: {script_file}")
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    print("--- STDOUT ---")
    print(process.stdout)
    if process.stderr:
        print("--- STDERR ---")
        print(process.stderr)
        
    if process.returncode != 0:
        print(f"[!] Blender exited with return code: {process.returncode}")
        sys.exit(process.returncode)
    else:
        print("[+] Execution completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/blender_runner.py <script_file.py> [args...]")
        sys.exit(1)
        
    script_arg = sys.argv[1]
    extra = sys.argv[2:] if len(sys.argv) > 2 else []
    run_blender_script(script_arg, extra)
