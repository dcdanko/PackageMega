"""File subclass sourced from a constructor hook."""

from .file import PMFile


class ConstructedFile(PMFile):
    """File subclass sourced from a constructor hook."""

    def __init__(self, *args, hook=None, **kwargs):
        """Initialize by storing the constructor hook."""
        super().__init__(*args, **kwargs)
        self.hook = hook

    def _resolver(self):
        """Return constructor hook."""
        return self.hook

    def _resolve_actual_file(self):
        """Resolve file by calling hook."""
        return self.hook()
