from gimme_input import UserInput, BoolUserInput
from subprocess import check_output
import os.path
from .custom_errors import UnresolvableFileError


class SourceFile:

    def __init__(self, repo, filename, *args):
        self.filename = filename
        self.url = None
        if len(args) > 0:
            self.url = args[0]
        self._filepath = None
        self.repo = repo

    def _downloadFile(self):
        targetPath = os.path.join(self.repo.downloadDir(), self.filename)
        cmd = 'wget {} -O {}'.format(self.url, targetPath)
        check_output(cmd, shell=True)
        return targetPath

    def _askUserForFile(self):
        _filepath = None
        msg = 'Is {} already on this system?'.format(self.filename)
        if self.url is None or BoolUserInput(msg, False).resolve():
            msg = 'Please indicate where {} is stored'.format(self.filename)
            _filepath = UserInput(msg).resolve()
        return _filepath

    def resolve(self):
        actualFile = self._askUserForFile()
        if actualFile is None and self.url is not None:
            actualFile = self._downloadFile()
        if actualFile is None:
            raise UnresolvableFileError()
        self._filepath = os.path.abspath(actualFile)

    def filepath(self):
        return self._filepath
