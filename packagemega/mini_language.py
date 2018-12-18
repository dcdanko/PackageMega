"""Filepath support for PackageMega naming convention."""

import os.path
from .custom_errors import UnresolvableOperandError, UnresolvableOperandLevel


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
    if len(fs) == 1:
        return os.path.dirname(fs.values()[0])
    sections = []
    for path in fs.values():
        for i, section in enumerate(path.split('/')):
            while len(sections) <= i:
                sections.append([])
            sections[i].append(section)

    consensus = []
    for section in sections:
        inconsensus = True
        for other in section[1:]:
            if other != section[0]:
                inconsensus = False
                break
        if inconsensus:
            consensus.append(section[0])

    fdir = '/'.join(consensus)
    if fdir[0] != '/':
        fdir = '/' + fdir
    return fdir


def _processFullOperand(db, operand, subops):
    """
    Return a filepath based on <database>.<item>.<file>.

    should also accept 2 special commands for <file>: prefix and dir
    which return a shared <element> or fail if that does not exist.
    """
    fs = {}
    for r in db.results():
        if r.name != '.'.join(subops[:2]):
            continue
        for _, f in r.files():
            fs[f.name] = f.filepath()

    if subops[2] == 'prefix':
        return _filePrefix(fs)
    if subops[2] == 'dir':
        return _fileDir(fs)

    try:
        return fs[subops[2]]
    except KeyError:
        try:
            return fs[operand]
        except KeyError:
            raise UnresolvableOperandError(operand)


def processOperand(repo, operand, stringify=False):
    """Process a full PackageMega operand."""
    subops = operand.split('.')
    oplevel = len(subops)
    db = repo.database(subops[0])

    if oplevel == 1:
        return db.tree() if stringify else db

    if oplevel == 2:
        rs = {r.name: r for r in db.results()}
        out = []
        for k, v in rs.items():
            if str(k) == operand:
                out.append(v)
        if stringify:
            out = '\n'.join([el.tree() for el in out])
        return out

    if oplevel == 3:
        return _processFullOperand(db, operand, subops)

    raise UnresolvableOperandLevel(oplevel)
