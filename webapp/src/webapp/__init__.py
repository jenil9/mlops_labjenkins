import runpy
from pathlib import Path


def main() -> None:
    app_path = Path(__file__).resolve().parents[2] / 'appfile.py'
    if app_path.exists():
        runpy.run_path(str(app_path), run_name='__main__')
        return

    print('Hello from webapp!')
