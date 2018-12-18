"""PackageMega repository class."""

import inspect
import os.path
from os import listdir, symlink
from shutil import copyfile
from subprocess import call
import sys

import datasuper as ds

from .custom_errors import RecipeNotFoundError, InvalidRecipeURI


class Repo:
    """PackageMega repository class."""

    repo_dir_name = '.package_mega'

    def __init__(self, abspath):
        """Initialize with repository path."""
        self.abspath = abspath
        self.recipe_dir = os.path.join(self.abspath, 'recipes')
        self.staging_dir = os.path.join(self.abspath, 'staging')

    def add_recipes(self, uri, dev=False):
        """Add recipe(s) from URI."""
        if os.path.exists(uri):
            return self.add_from_local(uri)

        if 'git' in uri:
            return self.add_from_github(uri)

        raise InvalidRecipeURI(uri)

    def add_from_local(self, uri, dev=False):
        """Add recipe from local filepath."""
        if uri[-9:] == 'recipe.py':
            file_sources = [uri]
        else:
            file_sources = [os.path.join(uri, dir_file) for dir_file in listdir(uri)]
        out = []
        for file_source in file_sources:
            if file_source[-9:] == 'recipe.py':
                abs_path = os.path.abspath(file_source)
                target = os.path.basename(file_source)
                target = os.path.join(self.recipe_dir, target)
                if dev:
                    try:
                        symlink(abs_path, target)
                    except FileExistsError:
                        pass
                else:
                    copyfile(abs_path, target)
                out.append(self._recipe_name(file_source))
        return out

    def add_from_github(self, uri):
        """Add recipe from GitHub URI."""
        hname = uri.split('/')[-1].split('.')[0]
        dest = os.path.join(self.staging_dir, hname)
        cmd = 'git clone {} {}'.format(uri, dest)
        call(cmd, shell=True)
        self.add_from_local(dest)

    def _recipe_name(self, recipe_filename):  # pylint: disable=no-self-use
        if recipe_filename[-9:] == 'recipe.py':
            recipe_prefix = recipe_filename[:-9]
            if recipe_prefix[-1] in ['-', '_', '.']:
                recipe_prefix = recipe_prefix[:-1]
            return os.path.basename(recipe_prefix)

        raise InvalidRecipeURI('{} is not a recipe'.format(recipe_filename))

    def all_recipes(self):
        """Return set containing names of all recipes in repository."""
        out = set()
        for recipe in listdir(self.recipe_dir):
            try:
                recipe_name = self._recipe_name(recipe)
                out.add(recipe_name)
            except AssertionError:
                pass
        return out

    def make_recipe(self, recipe_name):
        """Create a recipe from the recipe name."""
        # check if we have the recipe
        # if not throw an error
        if recipe_name not in self.all_recipes():
            raise RecipeNotFoundError(recipe_name)
        # else run it
        recipe = self._load_recipe(recipe_name)
        recipe.make_recipe()

    def _load_recipe(self, recipe_name):
        # (sort of hacky)
        for recipe_file in listdir(self.recipe_dir):
            if recipe_file[: len(recipe_name)] == recipe_name:
                fname = os.path.join(self.recipe_dir, recipe_file)
                break
        cname = self._get_class_name(fname)
        import_name = os.path.basename(fname)[:-3]

        sys.path.append(os.path.dirname(fname))
        __import__(import_name)
        classes = inspect.getmembers(sys.modules[import_name], inspect.isclass)
        for name, class_module in classes:
            if name == cname:
                return class_module()

        raise RecipeNotFoundError(recipe_name)

    def _get_class_name(self, fname):  # pylint: disable=no-self-use
        recipe_str = open(fname).read()
        cname = None
        for line in recipe_str.split('\n'):
            if 'class' in line:
                cname = line.split()[1]
                cname = cname.split(':')[0]
                cname = cname.split('(')[0]
                break
        return cname

    def download_dir(self):
        """Get directory for storing PackageMega downloads."""
        try:
            return os.environ['PACKAGE_MEGA_DOWNLOADS']
        except KeyError:
            try:
                default_db_dir = os.path.join(self.abspath,
                                              'database_dir_location.txt')
                default_db_dir = open(default_db_dir).read()
                return default_db_dir
            except FileNotFoundError:
                default_db_dir = os.path.join(self.abspath, 'databases')
                return default_db_dir

    def all_databases(self):
        """Return list of all databases present in the repository."""
        out = []
        for database in self.ds_repo().sampleTable.getAll():
            out.append(database)
        return out

    def database(self, database_name):
        """Get database by name."""
        return self.ds_repo().sampleTable.get(database_name)

    def db_status(self):
        """Get status of underlying DataSuper repository."""
        return self.ds_repo().checkStatus()

    def save_files(self, recipe, sub_name, *filepaths, **kw_filepaths):  # pylint: disable=too-many-locals
        """Save a group of files to a recipe using the sub_name suffix."""
        file_sources = {}
        for i, filepath in enumerate(filepaths):
            file_sources[i] = filepath
        for key, value in kw_filepaths.items():
            file_sources[key] = value

        with self.ds_repo() as dsr:
            schema = recipe.resultSchema()[sub_name]

            file_recs = []
            ftypes = dictify(schema)
            for key, fpath in file_sources.items():
                fname = '{}.{}.{}'.format(recipe.name(), sub_name, key)
                print('{} {}'.format(fname, fpath))
                ftype = ftypes[key]
                dsr.addFileType(ftype)
                ds.makeFile(dsr, fname, fpath, ftype, modify=True)
                file_recs.append(fname)

            schema_name = '{}::{}'.format(recipe.name(), sub_name)
            dsr.addResultSchema(schema_name, schema)
            rname = '{}.{}'.format(recipe.name(), sub_name)
            result = ds.getOrMakeResult(dsr, rname, schema_name, file_recs)

            dsr.addSampleType('db')
            sample = ds.getOrMakeSample(dsr, recipe.name(), 'db')
            sample.addResult(result).save(modify=True)

    def ds_repo(self):
        """Return the underlying DataSuper repository."""
        return ds.Repo.loadRepo(self.abspath)

    @staticmethod
    def load_repo():
        """Load the system-wide PackageMega repository."""
        try:
            target_dir = os.environ['PACKAGE_MEGA_HOME']
        except KeyError:
            target_dir = os.environ['HOME']
        target_dir = os.path.join(target_dir, Repo.repo_dir_name)
        target_dir_path = os.path.abspath(target_dir)
        try:
            # Ignore the return value
            ds.Repo.loadRepo(target_dir_path)
        except FileNotFoundError:
            Repo._init_repo()
            return Repo.load_repo()
        return Repo(target_dir_path)

    @staticmethod
    def _init_repo():
        try:
            target_dir = os.environ['PACKAGE_MEGA_HOME']
        except KeyError:
            target_dir = os.environ['HOME']
        target_dir_path = os.path.abspath(target_dir)
        target_dir_path = os.path.join(target_dir_path, Repo.repo_dir_name)
        os.makedirs(target_dir_path)
        ds.Repo.initRepo(targetDir=target_dir_path)
        recipes_dir = os.path.join(target_dir_path, 'recipes')
        os.makedirs(recipes_dir)
        staging_dir = os.path.join(target_dir_path, 'staging')
        os.makedirs(staging_dir)
        databases_dir = os.path.join(target_dir_path, 'databases')
        os.makedirs(databases_dir)


def dictify(element):
    """Transform element of any type into dictionary."""
    if isinstance(element, list):
        return {i: sub for i, sub in enumerate(element)}
    if isinstance(element, dict):
        return element
    return {0: element}
