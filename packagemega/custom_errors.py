"""Custom PackageMega errors and exceptions."""


class UnresolvableOperandError(Exception):
    """Raised when database operand cannot be resolved."""


class UnresolvableOperandLevel(Exception):
    """Raised when too many operand levels are supplied."""


class UnresolvableFileError(Exception):
    """Raised when a file source cannot be resolved."""


class RecipeNotFoundError(Exception):
    """Raised when a missing recipe is requested."""


class InvalidRecipeURI(Exception):
    """Raised when an invalid recipe URI is supplied."""
