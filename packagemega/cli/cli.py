import click
from packagemega import Repo
import sys


@click.group()
def main():
    pass

###############################################################################


@main.command()
@click.option('-d/-n', '--dev/--normal', default=False,
              help='Install recipe with symlinks')
@click.argument('uri')
def add(dev, uri):
    repo = Repo.loadRepo()
    repo.addFromLocal(uri, dev=dev)

###############################################################################


@main.command()
@click.argument('name')
def install(name):
    repo = Repo.loadRepo()
    repo.makeRecipe(name)

###############################################################################


@main.group()
def view():
    pass


@view.command(name='recipe')
def viewRecipes():
    repo = Repo.loadRepo()
    for recipe in repo.allRecipes():
        print(recipe)


@view.command(name='database')
@click.argument('operands', nargs=-1)
def viewDatabase(operands):
    repo = Repo.loadRepo()
    if len(operands) == 0:
        for db in repo.allDatabases():
            print(db.name)
    for operand in operands:
        operand = operand.split('.')
        if len(operand) == 1:
            db = repo.database(operand[0])
            for f in db.files():
                print(f)
        if len(operand) == 2:
            db = repo.database(operand[0])
            for k, v in db.files():
                if str(k) == operand[1]:
                    print(v)
                    break


###############################################################################

if __name__ == '__main__':
    main()
