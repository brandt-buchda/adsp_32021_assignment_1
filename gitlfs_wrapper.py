import pandas as pd
import subprocess
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def run(command):
    subprocess.run(command, shell=True, text=True)

def commit_dataframe(data: pd.DataFrame, version: int):
    filename = f"dataset_v{version}.csv"
    filepath = DATA_DIR / filename

    data.to_csv(filepath, index=False)

    run(f"git add {filepath}")
    run(f"git commit -m 'Add dataset version {version}'")
    run(f"git tag v{version}")
    run(f"git push origin main --tags")

def load_dataframe(version: int) -> pd.DataFrame:
    run(f"git checkout v{version}")
    filepath = DATA_DIR / f"dataset_v{version}.csv"
    return pd.read_csv(filepath)
