import os
from dotenv import load_dotenv

class EnvFileLoadError(Exception):
    pass

def load_env():
    dotenv_files = ['.env', os.path.join(os.pardir, '.env')]

    for dotenv_path in dotenv_files:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            return

    raise EnvFileLoadError(".env file not found in current or parent directory")
