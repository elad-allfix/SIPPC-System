"""Live tests call the real model through the user's Claude subscription.

They use real plan usage, so they only run when ALLFIX_LIVE=1.
"""
import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("ALLFIX_LIVE") == "1":
        return
    skip = pytest.mark.skip(reason="live model test; set ALLFIX_LIVE=1 to run")
    for item in items:
        if "/live/" in str(item.fspath):
            item.add_marker(skip)
