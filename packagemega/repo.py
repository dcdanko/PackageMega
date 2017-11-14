import os.path
import datasuper as ds


class RecipeNotFoundError( Exception):
    pass

class Repo:
    repoDirName = '.package_mega'
    resultSchemaRoot = 'result-schemas.yml'
    fileTypesRoot = 'file-types.yml'
    sampleTypesRoot = 'sample-types.yml'
    
    def __init__(self, abspath, dsRepo):
        self.abspath = abspath
        self.dsRepo = dsRepo


    def addRecipes(self, uri):
        pass
    
    def makeRecipe(self, recipeName):
        # check if we have the recipe
        # if not throw an error
        # else run it
        
    def allDatabases(self):
        out =[]
        for database in self.dsRepo.sampleTable.getAll():
            out.append(database)
        return out

    def database(self, databaseName):
        return self.dsRepo.sampleTable.get( databaseName)

    def saveFiles( recipe, subName, *filepaths):
        with self.dsRepo as dsr:
            sample = ds.SampleRecord(dsr,
                                  name=recipe.name(),
                                  sample_type='db')
            sample = sample.save(modify=True)
            for fType in recipe.fileTypes():
                dsr.addFileType( fType)
            schema = recipe.resultSchema[subName]
            dsr.addResultSchema(subName, schema)
            result = ds.ResultRecord(dsr,
                                  name=subName,
                                  result_type=subName,
                                  file_records=filepaths)
            result.save(modify=True)
            sample.addResult( result)
            sample.save(modify=True)

    @staticmethod
    def loadRepo():
        try:
            targetDir = os.environ['PACKAGE_MEGA_HOME']
        except KeyError:
            targetDir = os.environ['HOME']
        targetDir = os.path.join(targetDir, Repo.repoDirName)
        p = os.path.abspath(targetDir)
        try:
            dsRepo = ds.Repo.loadRepo(p)
        except ds.NoRepoFoundError():
            Repo._initRepo()
            return Repo.loadRepo()
        return Repo(p, dsRepo)

        
    @staticmethod
    def _initRepo():
        try:
            targetDir = os.environ['PACKAGE_MEGA_HOME']
        except KeyError:
            targetDir = os.environ['HOME']
        targetDir = os.path.join(targetDir, Repo.repoDirName)            
        p = os.path.abspath(targetDir)
        p = os.path.join(p, Repo.repoDirName)
        os.makedirs( p)
        ds.Repo.initRepo(targetDir=p)
        
                
