from cparsers.status import Status

def test_status():
    status = Status(["hello", "world"])
    assert status.result == None
    status = status.chainResult("ok", 0)
    assert status.result == "ok"

