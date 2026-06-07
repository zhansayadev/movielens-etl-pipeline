import requests, zipfile, os, io

MOVIELENS_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
DATA_DIR = "data/raw"

def download_movielens():
    """Download MovieLens small dataset and extract CSVs."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading MovieLens dataset...")
    resp = requests.get(MOVIELENS_URL, timeout=30)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        for name in z.namelist():
            if name.endswith(".csv"):
                filename = os.path.basename(name)
                with z.open(name) as src, open(f"{DATA_DIR}/{filename}", "wb") as dst:
                    dst.write(src.read())
                print(f"Extracted: {filename}")

    print("Extract complete.")

if __name__ == "__main__":
    download_movielens()
