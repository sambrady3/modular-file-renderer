# -*- coding: utf-8 -*-
import os
import mfr
import unittest
import pytest
import sys
from player import create_app
from flask import url_for  # NOQA


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.FILES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
        self.app = create_app(
            TESTING=True,
            FILES_DIR=self.FILES_DIR
        ).test_client()

    @pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7+")
    def test_index_request(self):
        index = self.app.get('/')
        assert index.status_code == 200
        data = index.get_data()
        for filename in os.listdir(self.FILES_DIR):
            if filename.startswith('.'):
                assert filename not in str(data)
            else:
                assert filename in str(data)

    @pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7+")
    def test_render_request(self):
        for filename in os.listdir(self.FILES_DIR):
            fp = open(os.path.join(self.FILES_DIR, filename))
            status_code = self.app.get(
                '/render/{filename}'.format(filename=filename)).status_code
            if mfr.detect(fp, many=False):
                assert status_code == 200
            else:
                assert status_code == 400

    @pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7+")
    def test_render_return_type(self):
        for filename in os.listdir(self.FILES_DIR):
            fp = open(os.path.join(self.FILES_DIR, filename))
            renderer = mfr.detect(fp, many=False)
            if renderer:
                # src = url_for('render.serve_file', filename=filename)
                result = mfr.render(fp)
                assert type(result) == mfr.RenderResult

    @pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7+")
    def test_file_serve_request(self):
        for filename in os.listdir(self.FILES_DIR):
            assert self.app.get(
                '/files/{filename}'.format(filename=filename)).status_code == 200
