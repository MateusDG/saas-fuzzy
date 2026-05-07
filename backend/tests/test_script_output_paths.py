from pathlib import Path

import pytest

from app.evaluation.preprocess_amazon_reviews_2023 import (
    PROJECT_ROOT as PREPROCESS_PROJECT_ROOT,
    resolve_path as resolve_preprocess_path,
)
from app.freeze_v0_baseline import (
    PROJECT_ROOT as FREEZE_PROJECT_ROOT,
    resolve_output_path as resolve_freeze_output_path,
)


def test_freeze_reports_path_stays_inside_repository_root() -> None:
    output_path = resolve_freeze_output_path(Path("reports/baselines/path_test.json"))
    assert output_path == (FREEZE_PROJECT_ROOT / "reports" / "baselines" / "path_test.json").resolve()


def test_freeze_normalizes_single_parent_prefix_for_legacy_backend_command() -> None:
    output_path = resolve_freeze_output_path(Path("../reports/baselines/path_test.json"))
    assert output_path == (FREEZE_PROJECT_ROOT / "reports" / "baselines" / "path_test.json").resolve()


def test_freeze_rejects_relative_path_that_escapes_repository_root() -> None:
    with pytest.raises(ValueError, match="escapes repository root"):
        resolve_freeze_output_path(Path("../../outside/path_test.json"))


def test_preprocess_output_dir_normalizes_single_parent_prefix() -> None:
    output_dir = resolve_preprocess_path(Path("../data/public/processed"), label="output")
    assert output_dir == (PREPROCESS_PROJECT_ROOT / "data" / "public" / "processed").resolve()
