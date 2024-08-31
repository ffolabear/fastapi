from unittest import mock

import mod2


def test_caller_a():
    with mock.patch("mod1.preamable", return_value=""):
        assert "11" == mod2.summer(5, 6)


def test_caller_b():
    with mock.patch("mod1.preamable") as mock_preamable:
        mock_preamable.return_value = ""
        assert "11" == mod2.summer(5, 6)


@mock.patch("mod1.preamable", return_value="")
def test_caller_c(mock_preamable):
    assert "11" == mod2.summer(5, 6)


@mock.patch("mod1.preamable")
def test_caller_d(mock_preamable):
    mock_preamable.return_value = ""
    assert "11" == mod2.summer(5, 6)