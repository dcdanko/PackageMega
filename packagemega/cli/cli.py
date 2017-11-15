import click
from packagemega import Repo
import sys

@click.group()
def main():
    pass

################################################################################
        
@main.group()
@click.option('-d/-n', '--dev/--normal', default=False, help='Install with symlinks')
@click.argument('uri')
def add(dev, uri):
    repo = Repo.loadRepo()
    repo.addFromLocal(uri, dev=dev)

################################################################################

@main.group()
def view():
    pass

@view.group(name='database')
def viewRecipes():
    repo = Repo.loadRepo()
    for recipe in repo.allRecipes():
        print(recipe)

@view.group(name='database')
@click.argument('operand', required=False)
def viewDatabase(operand=''):
    operand = operand.split('.')
    repo = Repo.loadRepo()
    if len(operand) == 0:
        for db in repo.allDatabases():
            print(db.name)
    if len(operand) == 1:
        db = repo.database( operand[0])
        for f in db.files():
            print(f)
    if len(operand) == 2:
        db = repo.database( operand[0])
        for k,v in db.files():
            if str(k) == operand[1]:
                print(v)
                break
        
        
        
        
    
################################################################################

if __name__ == '__main__':
    main()
