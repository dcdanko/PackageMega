import click
from packagemega import Repo
import sys
import os.path


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


def filePrefix(fs):
    out = ''
    for i in min([len(fpath for fpath in fs.values())]):
        cs = [fpath[i] for fpath in fs.values()]
        consensus = True
        for j in range(len(cs) - 1):
            if cs[j] != cs[j + 1]:
                consensus = False
                break
        if consensus:
            out += cs[0]
        else:
            break
    return out


def fileDir(fs):
    fdirs = [os.path.dirname(fpath) for fpath in fs.values()]
    consensus = True
    if len(fdirs) > 1:
        for a, b in zip(fdirs[1:], fdirs[:-1]):
            if a != b:
                consensus = False
                break
    if consensus:
        return fdirs[0]
    return ''


def processFullOperand(db, operand, subops):
    '''
    Returns a filepath based on <database>.<item>.<file>

    should also accept 2 special commands for <file>: prefix and dir
    which return a shared <element> or fail if that does not exist
    '''
    fs = {}
    for r in db.results():
        for k, f in r.files():
            fs[f.name] = f.filepath()
    if subops[2] == 'prefix':
        print(filePrefix(fs))
    elif subops[2] == 'dir':
        print(fileDir(fs))
    else:
        try:
            print(fs[subops[2]])
        except KeyError:
            print('{} not found.'.format(operand), file=sys.stderr)


def processOperand(repo, operand):
    subops = operand.split('.')
    oplevel = len(subops)
    db = repo.database(operand)
    if oplevel == 1:
        print(db.tree())
    elif oplevel == 2:
        rs = {r.name: r for r in db.results()}
        for k, v in rs.items():
            if str(k) == operand:
                    print(v.tree())
    elif oplevel == 3:
        processFullOperand(db, operand, subops)


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
        processOperand(repo, operand)


###############################################################################

if __name__ == '__main__':
    main()
