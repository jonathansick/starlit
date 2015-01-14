#!/usr/bin/env python
# encoding: utf-8
"""
Tests for the TexEncoder class.
"""

import pytest
from starlit.texutils import TexEncoder


@pytest.fixture
def encoder():
    return TexEncoder()


def test_latex_unicode(encoder):
    assert encoder.decode_latex(u"\&") == u"&"


def test_unicode_latex(encoder):
    assert encoder.encode_latex(u"&") == u"\&"
