


class SourceFile:

    def __init__(self, repo, filename, url):
        self.filename = filename
        self.url = url
        self._filepath = None
        
    def _downloadFile(self):
        pass

    def _askUserForFile(self):
        pass

    def resolve(self):
        actualFile = self._askUserForFile()
        if actualFile is None:
            actualFile = self._downloadFile()
        self._filepath = actualFile

    def filepath(self):
        return self._filepath
