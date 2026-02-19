import shutil
from pathlib import Path

import pytest

DOCS_TESTS_DIR = Path("docs/tests")


@pytest.fixture(scope="session", autouse=True)
def clean_docs_tests():
    if DOCS_TESTS_DIR.exists():
        shutil.rmtree(DOCS_TESTS_DIR)


@pytest.fixture(autouse=True)
def per_test_figure_saver(request):
    if request.cls is None:
        yield
        return
    request.cls._figures = []
    yield
    figures = request.cls._figures
    if figures:
        class_dir = DOCS_TESTS_DIR / request.cls.__name__
        class_dir.mkdir(parents=True, exist_ok=True)
        path = class_dir / f"{request.node.name}.md"
        path.write_text("\n\n".join(str(f) for f in figures) + "\n", encoding="utf-8")
