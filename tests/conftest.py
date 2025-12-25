import pytest
import sys
import os
from pathlib import Path

# Ensure src is in the path
src_path = Path(__file__).parents[1] / "src"
sys.path.insert(0, str(src_path))

from ckb_g2p.converter import Converter

@pytest.fixture(scope="session")
def converter():
    """
    Returns a shared Converter instance for all tests.
    Cache is DISABLED to ensure we test the logic, not the database.
    """
    return Converter(use_cache=False)