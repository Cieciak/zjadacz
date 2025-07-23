import pytest

from cparsers.status  import Status
from cparsers.error   import ParserError
from cparsers.parser  import Parser
from cparsers.helpers import *
from cparsers import string

def test_future_parser():
    with pytest.raises(RuntimeError) as err_info:
        parser = future()
        parser.run(Status('hello'))

    assert err_info.value.args[0] == 'transformer is not defined'

    