from cparsers.status import Status

def test_status():
    status = Status(["hello", "world"])
    assert status.result == None
    status = Status.result("ok", status=status)
    assert status.result == "ok"

