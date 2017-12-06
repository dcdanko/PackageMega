from gimme_input import UserInput, BoolUserInput
from .custom_errors import UnresolvableFileError
import os.path

class ConstructedFile:

    def __init__(self, repo, filename, *args):
        self.filename = filename
        self.hook = None
        if len(args) > 0:
            self.hook = args[0]
        self._filepath = None
        self.repo = repo

    def _askUserForFile(self):
        _filepath = None
        msg = 'Is {} already on this system?'.format(self.filename)
        if self.hook is None or BoolUserInput(msg, False).resolve():
            msg = 'Please indicate where {} is stored'.format(self.filename)
            _filepath = UserInput(msg).resolve()
        return _filepath

    def resolve(self):
        actualFile = self._askUserForFile()
        if actualFile is None and self.hook is not None:
            actualFile = self.hook()
        if actualFile is None:
            raise UnresolvableFileError()
        self._filepath = os.path.abspath(actualFile)

    def filepath(self):
        return self._filepath
