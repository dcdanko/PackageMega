from packagemega import BaseRecipe, SourceFile


class MycoTuberRecipe(BaseRecipe):

    def __init__(self):
        super(MycoTuberRecipe, self).__init__()
        self.source = SourceFile(self.repo, "mycobacterium_tubercoulosis.fna.gz", None)

    def name(self):
        return 'myco_tuber'

    def fileTypes(self):
        return ['gz_fasta_nucl']

    def resultSchema(self):
        return {
            'fasta': 'gz_fasta_nucl'
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
