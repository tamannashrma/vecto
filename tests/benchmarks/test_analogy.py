"""Tests for analogy benchmark."""

import contextlib
import unittest
import io
from os import path
from vecto.benchmarks.analogy import *
from vecto.benchmarks import visualize
from vecto.embeddings import load_from_dir
from ..test_setup import run_module


path_analogy_dataset = path.join('.', 'tests', 'data', 'benchmarks', 'analogy')


class Tests(unittest.TestCase):

    def test_api(self):
        embs = load_from_dir(path.join('tests', 'data', 'embeddings', 'text', 'plain_with_file_header'))
        analogy = LinearOffset()
        result = analogy.get_result(embs, path_analogy_dataset)
        self.assertIsInstance(result[0], dict)

        analogy = PairDistance()
        result = analogy.get_result(embs, path_analogy_dataset)
        self.assertIsInstance(result[0], dict)

        analogy = ThreeCosMul()
        result = analogy.get_result(embs, path_analogy_dataset)
        self.assertIsInstance(result[0], dict)

        analogy = ThreeCosMul2()
        result = analogy.get_result(embs, path_analogy_dataset)
        self.assertIsInstance(result[0], dict)

        analogy = ThreeCosAvg()
        result = analogy.get_result(embs, path_analogy_dataset)
        self.assertIsInstance(result[0], dict)

        # analogy = SimilarToAny()
        # result = analogy.get_result(embs, path_analogy_dataset)
        # print(result)
        # analogy = SimilarToB()
        # result = analogy.get_result(embs, path_analogy_dataset)
        # print(result)
        analogy = LRCos()
        result = analogy.get_result(embs, path_analogy_dataset)
        print(result)
        from matplotlib import pyplot as plt
        visualize.plot_accuracy("/tmp/vecto/benchmarks/analogy")
        plt.savefig("/tmp/vecto/benchmarks/analogy.pdf", bbox_inches="tight")

    def test_cli(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.analogy",
                       "./tests/data/embeddings/text/plain_with_file_header/",
                       "./tests/data/benchmarks/analogy/",
                       "--path_out", "/tmp/vecto/benchmarks/", "--method", "3CosAdd")

        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.analogy",
                       "./tests/data/embeddings/text/plain_with_file_header/",
                       "./tests/data/benchmarks/analogy/",
                       "--path_out", "/tmp/vecto/benchmarks/specific_filename.json",
                       "--method", "LRCos")

        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.analogy",
                       "./tests/data/embeddings/text/plain_with_file_header/",
                       "./tests/data/benchmarks/analogy/",
                       "--path_out", "/tmp/vecto/benchmarks/",
                       "--method", "3CosMul")

        sio = io.StringIO()
        with self.assertRaises(RuntimeError):
            with contextlib.redirect_stdout(sio):
                run_module("vecto.benchmarks.analogy",
                           "./tests/data/embeddings/text/plain_with_file_header/",
                           "./tests/data/benchmarks/analogy/",
                           "--method", "NONEXISTING")

        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.analogy",
                       "./tests/data/embeddings/text/plain_with_file_header/",
                       "./tests/data/benchmarks/analogy/",
                       "--method", "3CosAvg")
