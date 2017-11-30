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
            for r in db.results():
                fs = [el[1].filepath() for el in r.files()]
                o = '{}\t{}'.format(r.name, ' '.join(fs))
                print(o)
        if len(operand) == 2:
            db = repo.database(operand[0])
            rs = {r.resultType(): r for r in db.results()}
            for  k, v in rs.items():
                if str(k) == operand[1]:
                    fs = v.files()
                    if len(fs) == 1:
                        print(fs[0][1].filepath())
                    else:
                        for fname, f in v.files():
                            o = '{}\t{}'.format(fname, f.filepath())
                            print(o)
                    break


###############################################################################

if __name__ == '__main__':
    main()
