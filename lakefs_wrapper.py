import lakefs
from lakefs.client import Client
import pandas as pd

clt = Client(
    host="http://localhost:8000",
    username="AKIAIOSFOLQUICKSTART",
    password="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",)

REPO_NAME = "athletes"

if REPO_NAME not in [repo.id for repo in lakefs.repositories(client=clt)]:
    repo = lakefs.repository(REPO_NAME, client = clt).create(storage_namespace=f"local://{REPO_NAME}_v3")
else:
    repo = lakefs.repository(REPO_NAME, client = clt)

branch = lakefs.repository(REPO_NAME, client = clt).branch("main")


def commit_dataframe(data: pd.DataFrame, version: int):
    csv = data.to_csv(index=False).encode()

    try:
        with branch.transact(commit_message=f"add dataset version {version} (v{version})") as tx:
            tx.object(f"dataset version {version} (v{version}).csv").upload(csv)
    except Exception as e:
        print(e)
        pass

def load_dataframe(version: int)-> pd.DataFrame:
    csv_bytes = branch.object(f"dataset version {version} (v{version}).csv").reader()
    return pd.read_csv(csv_bytes)