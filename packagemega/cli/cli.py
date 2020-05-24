"""CLI command definitions."""

import os
import sys

import click
from packagemega import Repo
from packagemega.mini_language import process_operand
from packagemega.custom_errors import UnresolvableOperandError


version = {}  # pylint: disable=invalid-name
version_path = os.path.join(os.path.dirname(__file__), '../version.py')  # pylint: disable=invalid-name
with open(version_path) as version_file:
    exec(version_file.read(), version)  # pylint: disable=exec-used


@click.group()
@click.version_option(version['__version__'])
def main():
    """Enter PackageMega CLI."""


###############################################################################


def table_status(tbl_name, status_map):
    """Check if records in a table are valid and print a report to stdout."""
    sys.stdout.write('\n{} {}... '.format(len(status_map), tbl_name))
    all_good = True
    for name, status in status_map.items():
        if not status:
            all_good = False
            sys.stdout.write('\n - {} failed'.format(name))
    if all_good:
        sys.stdout.write('all good.')


@main.command(name='status')
def pm_status():
    """Print PackageMega repository status report to stdout."""
    repo = Repo.load_repo()
    sys.stdout.write('Checking status')
    for tbl_name, status_map in repo.db_status().items():
        table_status(tbl_name, status_map)
    sys.stdout.write('\nDone\n')

###############################################################################


@main.command()
@click.option('-d/-n', '--dev/--normal', default=False,
              help='Install recipe with symlinks')
@click.argument('uri')
def add(dev, uri):
    """Add URI to PackageMega repository."""
    repo = Repo.load_repo()
    repo.add_from_local(uri, dev=dev)

###############################################################################


@main.command()
@click.argument('name')
def install(name):
    """Install PackageMega recipe."""
    repo = Repo.load_repo()
    repo.make_recipe(name)

###############################################################################


@main.group()
def view():
    """Enter group of PackageMega view commands."""


@main.command(name='recipe')
def view_recipes():
    """View all recipes present in PackageMega repository."""
    repo = Repo.load_repo()
    for recipe in repo.all_recipes():
        print(recipe)

###############################################################################


def print_all_databases(repo):
    """Print the name of all databased present in repository."""
    for db in repo.all_databases():
        print(db.name)


@main.command(name='database')
@click.argument('operands', nargs=-1)
def view_database(operands):
    """Print database names filtered by operand arguments."""
    repo = Repo.load_repo()
    if not operands:
        print_all_databases(repo)
    for operand in operands:
        try:
            element = process_operand(repo, operand, stringify=True)
            print(element)
        except UnresolvableOperandError:
            print('{} could not be resolved.'.format(operand), file=sys.stderr)


###############################################################################

if __name__ == '__main__':
    main()
