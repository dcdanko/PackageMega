from subprocess import call


class HG19Recipe( BaseRecipe):

    def __init__(self):
        super(HG19Recipe, self).__init__()
        self.source = SourceFile(self.repo, "filename", "url")

    def name(self):
        return 'hg19'

    def fileTypes(self):
        return ['fasta', 'bt2_index']

    def resultSchema(self):
        return {
            'fasta': 'fasta',
            'bt2_index': ['bt2_index']*6
        }
    
    def makeRecipe(self):
        self.source.resolve()
        # after this point we will have the source file
        # either because we downloaded it or because the
        # user pointed it out.
        #
        # Multiple source files all need to be individually resolved
        self.repo.saveFiles(self,
                            'fasta',
                            self.source.filepath())
        
        bt2IndexFiles = self._makeBT2Index()
        self.repo.saveFiles(self,
                            'bt2',
                            bt2IndexFiles)

    def _makeBT2Index(self):
        base = self.source.filepath.split('.fa')[0]
        base += '.bt2'
        cmd = ('bowtie2-build ',
               '--threads ' + self.repo.numThreads(),
               self.source.filepath(),
               base)
        cmd = ' '.join(cmd)
        call(cmd, shell=True)
        return glob(base+'.*')
        
