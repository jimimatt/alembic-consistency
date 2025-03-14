from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from alembic_consistency.parse_migrations import (
    RevisionInfo,
    parse_alembic_file_content,
)
from alembic_consistency.consistency_check import (
    check_ordering_consistency,
    check_intrinsic_consistency,
)


def check_consistency(
    filenames: Sequence[str],
) -> int:
    revisions: list[RevisionInfo] = []
    for filename in filenames:
        file_content = Path(filename).read_text(encoding="utf-8")
        revisions.append(parse_alembic_file_content(file_content))

    ordering = check_ordering_consistency(revisions)
    intrinsic = check_intrinsic_consistency(revisions)

    return 0 if ordering and intrinsic else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+", help="Files to sort")

    args = parser.parse_args(argv)

    return check_consistency(args.filenames)


if __name__ == "__main__":
    raise SystemExit(main())
