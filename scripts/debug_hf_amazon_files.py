from huggingface_hub import HfApi

REPO_ID = "McAuley-Lab/Amazon-Reviews-2023"
api = HfApi()

revisions = [
    "main",
    "refs/pr/15",
    "refs/pr/24",
    "refs/pr/27",
]

keywords = [
    "Appliances",
    "raw_review_Appliances",
    "raw_meta_Appliances",
    "parquet",
]

for revision in revisions:
    print("\n" + "=" * 80)
    print(f"REVISION: {revision}")
    print("=" * 80)

    try:
        files = api.list_repo_files(
            repo_id=REPO_ID,
            repo_type="dataset",
            revision=revision,
        )
    except Exception as exc:
        print(f"ERRO ao listar {revision}: {exc}")
        continue

    matched = [
        f for f in files
        if any(k in f for k in keywords)
    ]

    print(f"Total de arquivos encontrados: {len(files)}")
    print(f"Arquivos relacionados a Appliances/parquet: {len(matched)}")

    for f in matched[:100]:
        print(f)