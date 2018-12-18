"""Base PackageMega recipe class."""

from .repo import Repo


class BaseRecipe:
    """Base PackageMega recipe class."""

    def __init__(self):
        """Initialize recipe."""
        self.repo = Repo.loadRepo()

    def makeRecipe(self):
        """Create the recipe."""
        raise NotImplementedError()
