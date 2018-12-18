"""Custom PackageMega errors and exceptions."""


class UnresolvableOperandError(Exception):
    pass


class UnresolvableOperandLevel(Exception):
    pass


class UnresolvableFileError(Exception):
    pass


class RecipeNotFoundError(Exception):
    pass


class InvalidRecipeURI(Exception):
    pass
