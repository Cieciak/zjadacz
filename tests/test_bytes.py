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

def test_uint8():
    p = bytesp.uint8()

    s1 = Status(bytearray([255, 0xBB, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))
    s2 = Status(bytes([255, 0xBB, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))

    r1 = p.run(s1)
    r2 = p.run(s2)

    assert r1.result == 255
    assert r2.result == r1.result

def test_uint16():
    p1 = bytesp.uint16('msb')
    p2 = bytesp.uint16('lsb')

    s1 = Status(bytearray([4, 0, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))
    s2 = Status(bytes([4, 0, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD]))

    r11 = p1.run(s1)
    r12 = p1.run(s2)
    
    r21 = p2.run(s1)
    r22 = p2.run(s2)

    assert r11.result == 1024
    assert r12.result == r11.result

    assert r21.result == 4
    assert r22.result == r21.result

def test_uint32():
    p1 = bytesp.uint32('msb')
    p2 = bytesp.uint32('lsb')

    s1 = Status(bytearray([0, 0, 4, 0, 0xAA, 0xBB, 0xCC, 0xDD]))
    s2 = Status(bytes([0, 0, 4, 0, 0xAA, 0xBB, 0xCC, 0xDD]))

    r11 = p1.run(s1)
    r12 = p1.run(s2)
    
    r21 = p2.run(s1)
    r22 = p2.run(s2)

    assert r11.result == 1024
    assert r12.result == r11.result

    assert r21.result == 4 * 256**2
    assert r22.result == r21.result

def test_uint64():
    p1 = bytesp.uint64('msb')
    p2 = bytesp.uint64('lsb')

    s1 = Status(bytearray([0, 0, 0, 0, 0, 0, 4, 0]))
    s2 = Status(bytes([0, 0, 0, 0, 0, 0, 4, 0]))

    r11 = p1.run(s1)
    r12 = p1.run(s2)
    
    r21 = p2.run(s1)
    r22 = p2.run(s2)

    assert r11.result == 1024
    assert r12.result == r11.result

    assert r21.result == 4 * 256**6
    assert r22.result == r21.result