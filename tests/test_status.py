from cparsers.status import Status

def test_chaining_result():

    original = Status('hello there')
    final    = original.chainResult('chain-result', increment=2)

    assert original.result == None
    assert final.result == 'chain-result'