"""Tests for analogy benchmark."""

import contextlib
import unittest
import io
from os import path
from vecto.benchmarks.language_modeling import *
from vecto.benchmarks import visualize
from vecto.embeddings import load_from_dir
from tests.test_setup import run_module

path_emb = path.join('tests', 'data', 'embeddings', 'text', 'plain_with_file_header')


class Tests(unittest.TestCase):

    def test_api(self):
        embs = load_from_dir(path_emb)
        language_modeling = Language_modeling(method='lstm')
        result = language_modeling.get_result(embs)
        self.assertIsInstance(result[0], dict)
        print(result)

        language_modeling = Language_modeling(method='lr')
        result = language_modeling.get_result(embs)
        self.assertIsInstance(result[0], dict)
        print(result)

        language_modeling = Language_modeling(method='2FFNN')
        result = language_modeling.get_result(embs)
        self.assertIsInstance(result[0], dict)
        print(result)

        language_modeling = Language_modeling(method='rnn')
        result = language_modeling.get_result(embs)
        self.assertIsInstance(result[0], dict)
        print(result)

    def test_cli(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.language_modeling",
                       path_emb,
                       "--window_size", "5",
                       "--path_out", "/tmp/vecto/benchmarks/")

        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module("vecto.benchmarks.language_modeling",
                       path_emb,
                       "--method", "lr",
                       "--path_out", "/tmp/vecto/benchmarks/tmp")

        with self.assertRaises(FileNotFoundError):
            sio = io.StringIO()
            with contextlib.redirect_stdout(sio):
                run_module("vecto.benchmarks.language_modeling",
                           path_emb + "NONEXISTING",
                           "--path_out", "/tmp/vecto/benchmarks/")

        from matplotlib import pyplot as plt
        visualize.plot_accuracy("/tmp/vecto/benchmarks/language_modeling", key_secondary="experiment_setup.dataset")
        plt.savefig("/tmp/vecto/benchmarks/language_modeling.pdf", bbox_inches="tight")


Tests().test_cli()
