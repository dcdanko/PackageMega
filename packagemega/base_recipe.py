"""Base PackageMega recipe class."""

from .repo import Repo


class BaseRecipe:  # pylint: disable=too-few-public-methods
    """Base PackageMega recipe class."""

    def __init__(self):
        """Initialize recipe."""
        self.repo = Repo.load_repo()

    def make_recipe(self):
        """Create the recipe."""
        raise NotImplementedError()
