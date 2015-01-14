#!/usr/bin/env python
# encoding: utf-8
"""
Tests for the TexEncoder class.
"""

import pytest
from starlit.texutils import TexEncoder, parse_name


@pytest.fixture
def encoder():
    return TexEncoder()


def test_latex_unicode(encoder):
    assert encoder.decode_latex(u"\&") == u"&"


def test_unicode_latex(encoder):
    assert encoder.encode_latex(u"&") == u"\&"


def test_parse_name():
    assert parse_name(u"{Sick}, Jonathan") == (u"Sick", u"Jonathan")
