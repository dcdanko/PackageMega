"""Basic test suite for PackgeMega."""

import os

from packagemega import Repo


def test_create_repo(tmp_path):
    """Ensure repo can be created."""

    repo = Repo(tmp_path)
    assert repo
