"""Loads markdown sections and converts them to HTML."""
from pathlib import Path
import markdown


class ContentLoader:
    def __init__(self, directory: str):
        self.__dir = Path(directory)

    def __render(self, path: Path) -> str:
        return markdown.markdown(path.read_text(encoding="utf-8"),
                                 extensions=["extra", "sane_lists"])

    def load_sections(self) -> list[dict]:
        """Files are ordered by numeric prefix: 01-about.md, 02-..."""
        return [
            {"id": p.stem.split("-", 1)[-1], "html": self.__render(p)}
            for p in sorted(self.__dir.glob("*.md"))
        ]
