from pathlib import Path

import pytest

# Run all the tests in the package
pytest.main(['-vv', str(Path(__file__).parent)])
