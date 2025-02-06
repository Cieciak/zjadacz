from cparsers.status import Status

def test_result_from_status():

    original = Status('hello there')

    result = Status.result('this is the result', status=original, increment=2)

    assert original.result == result.result

def test_chaining_result():

    original = Status('hello there')
    final    = original.chainResult('chain-result', increment=2)

    assert original.result == None
    assert final.result == 'chain-result'