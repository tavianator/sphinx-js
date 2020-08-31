# -*- coding: utf-8 -*-
from io import open
from os.path import dirname, join
from shutil import rmtree
from unittest import TestCase
import sys

from sphinx.cmd.build import main as sphinx_main
from sphinx.util.osutil import cd


class SphinxBuildTestCase(TestCase):
    """Base class for tests which require a Sphinx tree to be built and then
    deleted afterward

    """
    @classmethod
    def setup_class(cls):
        """Run Sphinx against the dir adjacent to the testcase."""
        cls.docs_dir = join(cls.this_dir(), 'source', 'docs')
        with cd(cls.docs_dir):  # Matters only to keep test_build_ts tests passing. Remove once we clean that module up. Its cwd-sensitivity still means it doesn't work for actual users if the cwd isn't just right.
            if sphinx_main([cls.docs_dir, '-b', 'text', '-v', '-E', join(cls.docs_dir, '_build')]):
                raise RuntimeError('Sphinx build exploded.')

    @classmethod
    def teardown_class(cls):
        rmtree(join(cls.docs_dir, '_build'))

    @classmethod
    def this_dir(cls):
        """Return the path to the dir containing the testcase class."""
        # nose does some amazing magic that makes this work even if there are
        # multiple test modules with the same name:
        return dirname(sys.modules[cls.__module__].__file__)

    def _file_contents(self, filename):
        with open(join(self.docs_dir, '_build', '%s.txt' % filename),
                  encoding='utf8') as file:
            return file.read()

    def _file_contents_eq(self, filename, contents):
        assert self._file_contents(filename) == contents
