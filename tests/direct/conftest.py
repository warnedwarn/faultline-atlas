from pathlib import Path
import pytest

@pytest.fixture
def contract_path():
    return Path(__file__).parents[2] / "contracts" / "contract.py"
