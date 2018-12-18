"""Basic test suite for PackgeMega."""

from packagemega import Repo


def test_create_repo(tmp_path):
    """Ensure repo can be created."""

    tmp_path = str(tmp_path)
    repo = Repo(tmp_path)
    assert repo
