"""Tests for library generation functionality."""

import logging
import os
import tempfile
from datetime import UTC, datetime
from os.path import join

import pytest

from ldraw import LibraryImporter, generate
from ldraw.colour import Colour
from ldraw.config import Config

logger = logging.getLogger(__name__)


@pytest.fixture
def test_ldraw_library():
    generated_path = tempfile.mkdtemp(prefix=datetime.now(UTC).isoformat())
    logger.debug(f"generated_path={generated_path}")
    config = Config(
        ldraw_library_path=os.path.join("tests", "test_ldraw"),
        generated_path=generated_path,
    )
    generate(config)
    LibraryImporter.set_config(config)
    return config.generated_path


def test_library_gen_files(test_ldraw_library) -> None:
    """Generated library contains the right files."""
    content = {
        os.path.relpath(os.path.join(dp, f), test_ldraw_library)
        for dp, dn, fn in os.walk(test_ldraw_library)
        for f in fn
    }

    library = {
        "__init__.py",
        "colours.py",
        "license.txt",
        "__hash__",
        join("parts", "__init__.py"),
        join("parts", "bricks.py"),
    }

    assert content == {join("library", el) for el in library}


def test_library_gen_import(test_ldraw_library) -> None:
    """Generated library is importable."""
    from ldraw import library

    assert set(library.__all__) == {"parts", "colours"}

    # Import parts module explicitly (can't access as attribute with dynamic imports)
    from ldraw.library import parts
    assert parts.__all__ == ["bricks"]
    assert {t for t in dir(parts) if not t.startswith("__")} == {
        "bricks",
        "Brick2X4",
    }

    from ldraw.library.parts import Brick2X4

    assert Brick2X4 == "3001"

    from ldraw.library.parts.bricks import Brick2X4

    assert Brick2X4 == "3001"

    from ldraw.library.colours import ColoursByCode, ColoursByName, Reddish_Gold

    expected_color = Colour(189, "Reddish_Gold", "#AC8247", 255, ["PEARLESCENT"])

    assert ColoursByCode == {expected_color.code: expected_color}
    assert ColoursByName == {expected_color.name: expected_color}

    assert Reddish_Gold == expected_color
