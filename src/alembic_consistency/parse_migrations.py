import re
import json
from dataclasses import dataclass
from typing import NewType


RevisionID = NewType("RevisionID", str)


@dataclass
class RevisionInfo:
    message: str
    revision_doc: str
    down_revision_doc: str
    create_date: str
    revision: RevisionID
    down_revision: RevisionID | None

    def __str__(self) -> str:
        return str(json.dumps(self.__dict__, indent=2))

    def is_consistent(self) -> bool:
        if self.revision == "":
            print(f"Revision ID is empty for message: {self.message}")
            return False
        if self.down_revision is None:
            return self.revision_doc == self.revision and self.down_revision_doc == ""
        return (
            self.revision_doc == self.revision
            and self.down_revision_doc == self.down_revision
        )


revision_regex = re.compile(r"revision\s*(?::\s*str\s*)?=\s*([\"\'])([^\"\']+)\1")
down_revision_regex = re.compile(
    r"down_revision\s*(?::\s*[^=]+)?=\s*([\"\'])([^\"\']+)\1"
)


def _extract_revision(text: str) -> RevisionID | None:
    match = re.search(revision_regex, text)
    return RevisionID(match.group(2)) if match else None


def _extract_down_revision(text: str) -> RevisionID | None:
    match = re.search(down_revision_regex, text)
    return RevisionID(match.group(2)) if match else None


def parse_alembic_file_content(text: str) -> RevisionInfo:
    """
    Parse an Alembic migration file generated from the given Mako template
    to extract:
      - message
      - up_revision (Revision ID)
      - down_revision (Revises)
      - create_date (Create Date)
      - revision (Python variable)
      - down_revision (Python variable)
    """
    # 1) Extract the docstring portion (including message, up_revision, down_revision, create_date)
    #    For simplicity, we assume it starts with triple quotes and ends right before the next triple quote.
    #    Then we can parse the lines inside it.
    docstring_match = re.search(r'"""(.*?)"""', text, re.DOTALL)
    docstring = docstring_match.group(1).strip() if docstring_match else ""

    # Extract lines from docstring
    # We expect lines like:
    #   Revision ID: ...
    #   Revises: ...
    #   Create Date: ...
    # plus anything before that as the "message."
    revision_id = ""
    down_revision_simple = ""
    create_date = ""
    message = ""

    # A quick approach: split the docstring by newlines, then parse line by line
    lines = [line.strip() for line in docstring.splitlines()]

    # The Mako template structure inside docstring is typically:
    #
    #   ${message}
    #
    #   Revision ID: ${up_revision}
    #   Revises: ${down_revision}
    #   Create Date: ${create_date}
    #
    # So the lines before "Revision ID:" can be concatenated as the 'message'.
    #
    # We'll simply iterate and capture the relevant fields:
    capture_message = True
    message_lines = []
    for line in lines:
        if line.startswith("Revision ID:"):
            revision_id = line[len("Revision ID:") :].strip()
            capture_message = False
        elif line.startswith("Revises:"):
            down_revision_simple = line[len("Revises:") :].strip()
        elif line.startswith("Create Date:"):
            create_date = line[len("Create Date:") :].strip()
        elif capture_message:
            # Accumulate lines into message
            message_lines.append(line)

    # Join any message lines that occurred before "Revision ID:"
    message = "\n".join(message_lines).strip()

    # 2) Extract the python-literal fields: revision, down_revision, branch_labels, depends_on
    revision_var = _extract_revision(text) or RevisionID("")
    down_revision_var = _extract_down_revision(text)

    return RevisionInfo(
        message=message,
        revision_doc=revision_id,
        down_revision_doc=down_revision_simple,
        create_date=create_date,
        revision=revision_var,
        down_revision=down_revision_var,
    )


if __name__ == "__main__":
    # Path to the generated migration file
    example_file = "../../tests/cases/vanilla/2024_12_24_2000-a8f4b7e2c1d6_create_superhero_schema.py"

    info = parse_alembic_file_content(example_file)
    print(info)
