from pathlib import Path
import shutil

from huggingface_hub import hf_hub_download


REPO_ID = "McAuley-Lab/Amazon-Reviews-2023"

REPO_ROOT = Path(__file__).resolve().parents[1]

OUT_DIR = REPO_ROOT / "data" / "public" / "raw"
CACHE_DIR = REPO_ROOT / "data" / "public" / "hf_cache"

OUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def download_file(filename: str, output_name: str) -> None:
    print(f"Baixando {filename}...")

    downloaded_path = hf_hub_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        filename=filename,
        revision="main",
        cache_dir=CACHE_DIR,
    )

    output_path = OUT_DIR / output_name

    print(f"Copiando para {output_path}...")
    shutil.copy2(downloaded_path, output_path)

    print(f"OK: {output_path}")


if __name__ == "__main__":
    download_file(
        "raw/review_categories/Appliances.jsonl",
        "Appliances.jsonl",
    )

    download_file(
        "raw/meta_categories/meta_Appliances.jsonl",
        "meta_Appliances.jsonl",
    )

    print("\nArquivos prontos em data/public/raw/")