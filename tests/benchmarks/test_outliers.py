"""Tests for outliers benchmark."""

import unittest
from io import StringIO
from contextlib import redirect_stdout
from vecto.benchmarks.outliers import *
from vecto.embeddings import load_from_dir
from ..test_setup import run_module

path_outliers_dataset = path.join('.', 'tests', 'data', 'benchmarks', 'outliers')


class Tests(unittest.TestCase):
    def test_outliers(self):
        embs = load_from_dir(path.join('tests', 'data', 'embeddings', 'text', 'plain_with_file_header'))
        outliers = AveragePairwiseCosine()
        result = outliers.get_result(embs, path_outliers_dataset)

    def test_cli(self):
        sio = StringIO()
        with redirect_stdout(sio):
            run_module('vecto.benchmarks.outliers',
                       './tests/data/embeddings/text/plain_with_file_header/',
                       './tests/data/benchmarks/outliers/',
                       '--path_out', '/tmp/vecto/', '--method', 'AveragePairwiseCosine')

    def test_outliers_results(self):
        embs = load_from_dir(path.join('tests', 'data', 'embeddings', 'text', 'plain_with_file_header'))
        outliers = AveragePairwiseCosine()
        result = outliers.get_result(embs, path_outliers_dataset)[0]
        amount_of_categories = 2
        amount_of_word_in_cats = 3

        self.assertEqual(len(result.keys()), amount_of_categories)
        self.assertEqual(len(result['cats']), amount_of_word_in_cats)