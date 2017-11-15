import os.path
import datasuper as ds
from os import listdir, symlink
from shutil import copyfile

class RecipeNotFoundError( Exception):
    pass

class Repo:
    repoDirName = '.package_mega'
    
    def __init__(self, abspath, dsRepo):
        self.abspath = abspath
        self.dsRepo = dsRepo
        self.recipeDir = os.path.join( self.abspath, 'recipes')
        self.stagingDir = os.path.join( self.abspath, 'staging')        

    def addRecipes(self, uri, dev=False):
        if os.path.exists(self.uri):
            return self.addFromLocal()
        elif 'git' in self.uri:
            return self.addFromGithub()
    
    def addFromLocal(self, uri, dev=False):
        recipes = []
        if uri[-9:] == 'recipe.py':
            if dev:
                symlink(f, self.recipeDir)
            else:
                copyfile(f, self.recipeDir)
            return
        
        for f in listdir(uri):
            if f[-9:] == 'recipe.py':
                if dev:
                    symlink(f, self.recipeDir)
                else:
                    copyfile(f, self.recipeDir)

    def addFromGithub(self, uri):
        hname = self.uri.split('/')[-1].split('.')[0]
        dest = os.path.join( self.stagingDir, hname)
        cmd = 'git clone {} {}'.format(self.uri, dest)
        call(cmd, shell=True)
        self.addFromLocal(dest)


    def allRecipes(self):
        out = set()
        for recipe in listdir(self.recipeDir):
            if recipe[-9:] == 'recipe.py':
                out.add( recipe[:-9])
        return out
    
    def makeRecipe(self, recipeName):
        # check if we have the recipe
        # if not throw an error
        if recipeName not in self.allRecipes():
            raise RecipeNotFoundError()
        # else run it 
        recipe.makeRecipe()

        
    def _loadRecipe(self, recipeName):
        # (sort of hacky)
        fname = os.path.join( self.recipeDir, recipeName + 'recipe.py')
        recipeStr = open(fname).read()
        cname = None
        for line in recipeStr.split('\n'):
            if 'class' in line:
                cname = line.split()[1]
                cname.split(':')[0]
                cname.split('(')[0]
                break
            
        exec( recipeStr)
        exec( 'recipe = {}()'.format(cname))
        return recipe

        
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
        
                
