from pathlib import Path


def _is_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _normalize_single_parent_prefix(path: Path) -> Path | None:
    parts = list(path.parts)
    if len(parts) >= 2 and parts[0] == ".." and parts[1] not in {"..", "."}:
        return Path(*parts[1:])
    return None


def resolve_project_path(
    path: Path,
    project_root: Path,
    *,
    label: str,
) -> Path:
    root = project_root.resolve()

    if path.is_absolute():
        return path.resolve()

    direct = (root / path).resolve()
    if _is_within_root(direct, root):
        return direct

    normalized = _normalize_single_parent_prefix(path)
    if normalized is not None:
        normalized_path = (root / normalized).resolve()
        if _is_within_root(normalized_path, root):
            print(
                "[KouzinaReco] normalized relative "
                f"{label} path '{path}' to '{normalized}' to keep it inside the repository root."
            )
            return normalized_path

    raise ValueError(
        f"Relative {label} path '{path}' escapes repository root '{root}'. "
        "Use a repository-relative path like 'reports/...'."
    )
