from pathlib import Path

from alembic_consistency.parse_migrations import (
    parse_alembic_file_content,
    RevisionInfo,
)


def get_case_files(case: str) -> list[Path]:
    case_dir = Path(f"tests/cases/{case}")
    return list(case_dir.glob("*.py"))


def get_revision_infos(files: list[Path]) -> list[RevisionInfo]:
    revisions: list[RevisionInfo] = []
    for file in files:
        file_content = file.read_text(encoding="utf-8")
        revisions.append(parse_alembic_file_content(file_content))
    return revisions


def test_vanilla_ordering():
    from alembic_consistency.consistency_check import check_ordering_consistency

    revisions = get_revision_infos(get_case_files("vanilla"))
    assert check_ordering_consistency(revisions)


def test_missing_start():
    from alembic_consistency.consistency_check import check_ordering_consistency

    revisions = get_revision_infos(get_case_files("missing_start"))
    assert not check_ordering_consistency(revisions)


def test_broken_chain():
    from alembic_consistency.consistency_check import check_ordering_consistency

    revisions = get_revision_infos(get_case_files("broken_chain"))
    assert not check_ordering_consistency(revisions)


def test_ambiguous_successor():
    from alembic_consistency.consistency_check import check_ordering_consistency

    revisions = get_revision_infos(get_case_files("ambiguous_successor"))
    assert not check_ordering_consistency(revisions)


def test_inconsistent_start_script():
    from alembic_consistency.consistency_check import check_intrinsic_consistency

    revisions = get_revision_infos(get_case_files("inconsistent_start_script"))
    assert not check_intrinsic_consistency(revisions)


def test_inconsistent_script():
    from alembic_consistency.consistency_check import check_intrinsic_consistency

    revisions = get_revision_infos(get_case_files("inconsistent_script"))
    assert not check_intrinsic_consistency(revisions)


def test_vanilla_wrong_file_ordering():
    from alembic_consistency.consistency_check import check_intrinsic_consistency

    revisions = get_revision_infos(get_case_files("vanilla_wrong_file_ordering"))
    assert check_intrinsic_consistency(revisions)
