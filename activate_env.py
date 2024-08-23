import os
import subprocess

def activate_default_venv():
    """
    Activate the virtual environment in the default directory.
    """
    # Get the current working directory
    current_dir = os.getcwd()

    # Check if the virtual environment exists in the default directory
    venv_path = os.path.join(current_dir, 'venv')
    if os.path.isdir(venv_path):
        # Activate the virtual environment
        activate_script = os.path.join(venv_path, 'Scripts' if os.name == 'nt' else 'bin', 'activate')
        subprocess.run([activate_script], shell=True)
        print(f"Activated virtual environment in '{current_dir}'.")
    else:
        print(f"Virtual environment not found in '{current_dir}'.")

if __name__ == "__main__":
    activate_default_venv()
