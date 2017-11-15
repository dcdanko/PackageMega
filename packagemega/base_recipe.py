from .repo import Repo



class BaseRecipe:

    def __init__(self):
        self.repo = Repo.loadRepo()
        

    
    def makeRecipe(self):
        raise NotImplementedError()
        
