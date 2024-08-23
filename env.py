import os
import sys
import subprocess

def create_or_activate_venv():
    venv_name = 'venv'
    venv_path = os.path.join(os.getcwd(), venv_name)

    if os.path.isdir(venv_path):
        # If venv directory exists, activate it
        activate_script = os.path.join(venv_path, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
        subprocess.run([activate_script], shell=True)
        print(f"Activated existing virtual environment '{venv_name}'.")
    else:
        # Create new virtual environment
        subprocess.run([sys.executable, '-m', 'venv', venv_name])
        print(f"Created new virtual environment '{venv_name}'.")

if __name__ == "__main__":
    create_or_activate_venv()
