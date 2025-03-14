from collections import defaultdict

from alembic_consistency.parse_migrations import RevisionInfo, RevisionID


def get_first_revision(revisions: list[RevisionInfo]) -> RevisionInfo | None:
    for revision in revisions:
        if revision.down_revision is None:
            return revision
    return None


def get_successor(revisions: list[RevisionInfo], revision: str) -> RevisionInfo | None:
    for i, rev in enumerate(revisions):
        if revision == rev.down_revision:
            return revisions[i]
    return None


def check_ordering_consistency(revisions: list[RevisionInfo]) -> bool:
    first_revision: RevisionInfo | None = get_first_revision(revisions)
    if first_revision is None:
        print("No first revision found.")
        return False
    ordered_revisions: list[RevisionInfo] = [
        first_revision,
    ]

    revision_mapping: dict[RevisionID, list[RevisionID | None]] = defaultdict(list)
    for rev in revisions:
        if rev.down_revision is not None:
            revision_mapping[rev.down_revision].append(rev.revision)

    ambiguous_revisions = [
        rev for rev, down_revs in revision_mapping.items() if len(down_revs) > 1
    ]
    if ambiguous_revisions:
        print(f"Ambiguous revisions (with multiple successors): {ambiguous_revisions}")
        return False

    change = 1
    while change > 0:
        change = 0
        next_revision = get_successor(revisions, ordered_revisions[-1].revision)
        if next_revision is None:
            continue
        ordered_revisions.append(next_revision)
        change += 1
    if len(ordered_revisions) != len(revisions):
        print(
            f"Not all revisions are connected. Revision ID '{ordered_revisions[-1].revision}' has no successor."
        )
        return False

    return True


def check_intrinsic_consistency(revisions: list[RevisionInfo]) -> bool:
    inconsistent_revisions = [
        rev.revision for rev in revisions if not rev.is_consistent()
    ]
    if inconsistent_revisions:
        print(f"Inconsistent revisions: {inconsistent_revisions}")
        return False
    return True
