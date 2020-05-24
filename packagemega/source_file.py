"""File subclass sourced from a URI."""

import os.path
from subprocess import check_output

from .file import PMFile


class SourceFile(PMFile):
    """File subclass sourced from a URI."""

    def __init__(self, *args, url=None, **kwargs):
        """Initialize by storing the URI."""
        super().__init__(*args, **kwargs)
        self.url = url

    def _download_file(self):
        """Download the file."""
        target_path = os.path.join(self.repo.download_dir(), self.filename)
        cmd = 'wget {} -O {}'.format(self.url, target_path)
        check_output(cmd, shell=True)
        return target_path

    def _resolver(self):
        """Return file url."""
        return self.url

    def _resolve_actual_file(self):
        """Resolve file by downloading it."""
        return self._download_file()
