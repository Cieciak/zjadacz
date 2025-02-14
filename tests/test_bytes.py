from cparsers.status import Status
from cparsers.parser import Parser
import cparsers.bytes as bytesp

def test_byte():
    p = bytesp.byte()

    s1 = Status(bytearray([0xAA, 0xBB]))
    s2 = Status(bytes([0xAA, 0xBB]))

    r1 = p.run(s1)
    r2 = p.run(s2)

    assert r1.result == 170
    assert r2.result == r1.result

def test_word():
    p = bytesp.word()

    s1 = Status(bytearray([0xAA, 0xBB, 0xCC]))
    s2 = Status(bytes([0xAA, 0xBB, 0xCC]))

    r1 = p.run(s1)
    r2 = p.run(s2)

    assert r1.result == b'\xaa\xbb'
    assert r2.result == r1.result

def test_dword():
    p = bytesp.dword()

    s1 = Status(bytearray([0xAA, 0xBB, 0xCC, 0xDD]))
    s2 = Status(bytes([0xAA, 0xBB, 0xCC, 0xDD]))

    r1 = p.run(s1)
    r2 = p.run(s2)

    assert r1.result == b'\xaa\xbb\xcc\xdd'
    assert r2.result == r1.result

def test_qword():
    p = bytesp.qword()

    s1 = Status(bytearray([0xAA, 0xBB, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))
    s2 = Status(bytes([0xAA, 0xBB, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))

    r1 = p.run(s1)
    r2 = p.run(s2)

    assert r1.result == b'\xaa\xbb\xcc\xdd\xaa\xbb\xcc\xdd'
    assert r2.result == r1.result