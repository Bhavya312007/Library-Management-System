import os

def is_venv_active():
    """
    Check if a Python virtual environment is active.
    """
    # Check if the 'VIRTUAL_ENV' environment variable is set
    venv_path = os.environ.get('VIRTUAL_ENV')
    return venv_path is not None

if __name__ == "__main__":
    if is_venv_active():
        print("Virtual environment is active.")
    else:
        print("Virtual environment is not active.")
