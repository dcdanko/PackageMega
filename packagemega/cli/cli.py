import click
from packagemega import Repo
import sys
from pyarchy import archy


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
        noperand = len(operand.split('.'))
        if noperand == 1:
            db = repo.database(operand)
            print(db.tree())
        elif noperand == 2:
            dbName = operand.split('.')[0]
            db = repo.database(dbName)
            rs = {r.name: r for r in db.results()}
            for k, v in rs.items():
                if str(k) == operand:
                    print(v.tree())
        elif noperand == 3:
            dbName = operand.split('.')[0]
            db = repo.database(dbName)
            fs = {}
            for r in db.results():
                for k, f in r.files():
                    fs[f.name] = f.filepath()
            for k, v in fs.items():
                if k == operand:
                    print(v)


###############################################################################

if __name__ == '__main__':
    main()
