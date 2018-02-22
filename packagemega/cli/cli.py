import click
from packagemega import Repo
import sys
from packagemega.mini_language import processOperand
from packagemega.custom_errors import UnresolvableOperandError


@click.group()
def main():
    pass


###############################################################################


def tableStatus(tblName, statusMap):
    '''Check if records in a table are valid and print a report to stdout.'''
    sys.stdout.write('\n{} {}... '.format(len(statusMap), tblName))
    allGood = True
    for name, status in statusMap.items():
        if not status:
            allGood = False
            sys.stdout.write('\n - {} failed'.format(name))
    if allGood:
        sys.stdout.write('all good.')


@main.command()
def status():
    repo = Repo.loadRepo()
    sys.stdout.write('Checking status')
    for tblName, statusMap in repo.dbStatus().items():
        tableStatus(tblName, statusMap)
    sys.stdout.write('\nDone\n')

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
