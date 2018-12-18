"""CLI command definitions."""

import os
import sys

import click
from packagemega import Repo
from packagemega.mini_language import processOperand
from packagemega.custom_errors import UnresolvableOperandError


version = {}
version_path = os.path.join(os.path.dirname(__file__), '../version.py')
with open(version_path) as version_file:
    exec(version_file.read(), version)  # pylint: disable=exec-used


@click.group()
@click.version_option(version['__version__'])
def main():
    """Enter PackageMega CLI."""


###############################################################################


def tableStatus(tblName, statusMap):
    """Check if records in a table are valid and print a report to stdout."""
    sys.stdout.write('\n{} {}... '.format(len(statusMap), tblName))
    allGood = True
    for name, status in statusMap.items():
        if not status:
            allGood = False
            sys.stdout.write('\n - {} failed'.format(name))
    if allGood:
        sys.stdout.write('all good.')


@main.command(name='status')
def pm_status():
    """Print PackageMega repository status report to stdout."""
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
    """Add URI to PackageMega repository."""
    repo = Repo.loadRepo()
    repo.addFromLocal(uri, dev=dev)

###############################################################################


@main.command()
@click.argument('name')
def install(name):
    """Install PackageMega recipe."""
    repo = Repo.loadRepo()
    repo.makeRecipe(name)

###############################################################################


@main.group()
def view():
    """Enter group of PackageMega view commands."""


@main.command(name='recipe')
def viewRecipes():
    """View all recipes present in PackageMega repository."""
    repo = Repo.loadRepo()
    for recipe in repo.allRecipes():
        print(recipe)

###############################################################################


def printAllDatabases(repo):
    """Print the name of all databased present in repository."""
    for db in repo.allDatabases():
        print(db.name)


@main.command(name='database')
@click.argument('operands', nargs=-1)
def viewDatabase(operands):
    """Print database names filtered by operand arguments."""
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
