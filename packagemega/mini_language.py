import os.path
from .custom_errors import UnresolvableOperandError


def _filePrefix(fs):
    out = ''
    ls = [len(fpath) for fpath in fs.values()]
    for i in range(min(ls)):
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
    if out[-1] == '.':
        out = out[:-1]
    return out


def _fileDir(fs):
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


def _processFullOperand(db, operand, subops):
    '''
    Returns a filepath based on <database>.<item>.<file>

    should also accept 2 special commands for <file>: prefix and dir
    which return a shared <element> or fail if that does not exist
    '''
    fs = {}
    for r in db.results():
        if r.name != '.'.join(subops[:2]):
            continue
        for k, f in r.files():
            fs[f.name] = f.filepath()
    if subops[2] == 'prefix':
        return _filePrefix(fs)
    elif subops[2] == 'dir':
        return _fileDir(fs)
    else:
        try:
            return fs[subops[2]]
        except KeyError:
            try:
                return fs[operand]
            except KeyError:
                raise UnresolvableOperandError(operand)



def processOperand(repo, operand, stringify=False):
    subops = operand.split('.')
    oplevel = len(subops)
    db = repo.database(subops[0])

    if oplevel == 1:
        if stringify:
            return db.tree()
        else:
            return db

    elif oplevel == 2:
        rs = {r.name: r for r in db.results()}
        out = []
        for k, v in rs.items():
            if str(k) == operand:
                out.append(v)
        if stringify:
            out = '\n'.join([el.tree() for el in out])
        return out

    elif oplevel == 3:
        return _processFullOperand(db, operand, subops)
