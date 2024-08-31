import os

import mod2

os.environ["UNIT_TEST"] = "true"


def test_summer_fake():
    assert "11" == mod2.summer(5, 6)
