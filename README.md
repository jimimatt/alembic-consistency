# alembic inconsistency checker

[pre-commit](https://pre-commit.com/) hook to check [alembic](https://alembic.sqlalchemy.org/en/latest/) migration scripts for inconsistencies.

Assumptions for consistent migration scripts:
- one base migration script (down revision is null)
- migration scripts forming one contiguous, linear chain (all scripts are connected)

The algorithm is order independent, ordering of passed files is not important.

## Usage

Example `.pre-commit-config.yaml` (assuming alembic migration scripts are in `project/versions` directory):

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/jimimatt/alembic-consistency
    rev: v0.1.0
    hooks:
      - id: alembic-consistency-checker
        files: ^project/versions/.*\.py$
```

Parameter `files` defines which files should be checked.
Works the same way as `files` parameter for [file-contents-sorter](https://github.com/pre-commit/pre-commit-hooks/tree/main) pre-commit hook.


## How to solve multiple heads

Nice instructions on how to deal with multiple heads:  
[https://blog.jerrycodes.com/multiple-heads-in-alembic-migrations/](https://blog.jerrycodes.com/multiple-heads-in-alembic-migrations/)
