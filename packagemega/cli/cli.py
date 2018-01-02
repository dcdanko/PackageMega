import click
from packagemega import Repo
import sys
from packagemega.mini_language import processOperand
from packagemega.custom_errors import UnresolvableOperandError


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


@main.command(name='recipe')
def viewRecipes():
    repo = Repo.loadRepo()
    for recipe in repo.allRecipes():
        print(recipe)

###############################################################################


def printAllDatabases(repo):
    for db in repo.allDatabases():
        print(db.name)


@main.command(name='database')
@click.argument('operands', nargs=-1)
def viewDatabase(operands):
    repo = Repo.loadRepo()
    if len(operands) == 0:
        printAllDatabases(repo)
    for operand in operands:
        try:
            el = processOperand(repo, operand, stringify=True)
            print(el)
        except UnresolvableOperandError:
            print('{} could not be resolved.'.format(operand), file=sys.stderr)


###############################################################################

if __name__ == '__main__':
    main()
