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

    def _askUserForFile(self):
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
        actualFile = self._askUserForFile()
        if actualFile is None and self._resolver() is not None:
            actualFile = self._resolve_actual_file()
        if actualFile is None:
            raise UnresolvableFileError()
        self._filepath = os.path.abspath(actualFile)

    def filepath(self):
        """Expose private _filepath as read-only."""
        return self._filepath
