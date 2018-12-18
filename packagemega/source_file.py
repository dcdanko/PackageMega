
import os.path
from subprocess import check_output
from gimme_input import UserInput, BoolUserInput

from .custom_errors import UnresolvableFileError
from .file import PMFile


class SourceFile(PMFile):

    def __init__(self, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    def _downloadFile(self):
        targetPath = os.path.join(self.repo.downloadDir(), self.filename)
        cmd = 'wget {} -O {}'.format(self.url, targetPath)
        check_output(cmd, shell=True)
        return targetPath

    def _resolver(self):
        """Return file url."""
        return self.url

    def _resolve_actual_file(self):
        """Resolve file by downloading it."""
        return self._downloadFile()
