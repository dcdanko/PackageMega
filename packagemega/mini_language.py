"""Filepath support for PackageMega naming convention."""

import os.path
from .custom_errors import UnresolvableOperandError, UnresolvableOperandLevel


def _file_prefix(file_sources):
    out = ''
    path_lengths = [len(fpath) for fpath in file_sources.values()]
    for i in range(min(path_lengths)):
        components = [fpath[i] for fpath in file_sources.values()]
        consensus = True
        for j in range(len(components) - 1):
            if components[j] != components[j + 1]:
                consensus = False
                break
        if consensus:
            out += components[0]
        else:
            break
    if out[-1] == '.':
        out = out[:-1]
    return out


def _file_dir(file_sources):
    if len(file_sources) == 1:
        return os.path.dirname(file_sources.values()[0])
    sections = []
    for path in file_sources.values():
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


def _process_full_operand(db, operand, subops):
    """
    Return a filepath based on <database>.<item>.<file>.

    should also accept 2 special commands for <file>: prefix and dir
    which return a shared <element> or fail if that does not exist.
    """
    file_sources = {}
    for result in db.results():
        if result.name != '.'.join(subops[:2]):
            continue
        for _, result_file in result.files():
            file_sources[result_file.name] = result_file.filepath()

    if subops[2] == 'prefix':
        return _file_prefix(file_sources)
    if subops[2] == 'dir':
        return _file_dir(file_sources)

    try:
        return file_sources[subops[2]]
    except KeyError:
        try:
            return file_sources[operand]
        except KeyError:
            raise UnresolvableOperandError(operand)


def process_operand(repo, operand, stringify=False):
    """Process a full PackageMega operand."""
    subops = operand.split('.')
    oplevel = len(subops)
    db = repo.database(subops[0])

    if oplevel == 1:
        return db.tree() if stringify else db

    if oplevel == 2:
        results = {result.name: result for result in db.results()}
        out = []
        for key, value in results.items():
            if str(key) == operand:
                out.append(value)
        if stringify:
            out = '\n'.join([element.tree() for element in out])
        return out

    if oplevel == 3:
        return _process_full_operand(db, operand, subops)

    raise UnresolvableOperandLevel(oplevel)
