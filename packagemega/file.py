"""Base PackageMega file class."""

import os.path
from gimme_input import UserInput, BoolUserInput

from .custom_errors import UnresolvableFileError


class PMFile:
    """Base PackageMega file class."""

    def __init__(self, repo, filename, *args, **kwargs):
        """Initialze PMFile with repo and filename this file is to resolve to."""
        super().__init__(*args, **kwargs)
        self.repo = repo
        self.filename = filename
        self._filepath = None

    def _ask_user_for_file(self):
        """Prompt user for existing file path."""
        _filepath = None
        msg = 'Is {} already on this system?'.format(self.filename)
        if self._resolver() is None or BoolUserInput(msg, False).resolve():
            msg = 'Please indicate where {} is stored'.format(self.filename)
            _filepath = UserInput(msg).resolve()
        return _filepath

    def _resolver(self):
        """Return subclass-specific file resolver."""
        raise NotImplementedError()

    def _resolve_actual_file(self):
        """Resolve file in subclass-specific way."""
        raise NotImplementedError()

    def resolve(self):
        """Create file from subclass-specific resolver."""
        actual_file = self._ask_user_for_file()
        if actual_file is None and self._resolver() is not None:
            actual_file = self._resolve_actual_file()
        if actual_file is None:
            raise UnresolvableFileError()
        self._filepath = os.path.abspath(actual_file)

    def filepath(self):
        """Expose private _filepath as read-only."""
        return self._filepath
