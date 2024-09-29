import numpy as np

from utils import strToBytes, bytesToStr
from Cipher import S_DES

test = True
if test:

    str = "who are you"
    key = np.array([0, 1, 1, 0, 1, 0, 0, 0, 1, 1])
    x = strToBytes(str, False)
    print(bytesToStr(x, False))
    print("p: ", x)

    machine = S_DES()
    c = machine.forward(x, key, isEncrypt=True)
    print("c: ", c)
    print("c: ", bytesToStr(c, False))

    p = machine.forward(c, key, isEncrypt=False)
    print("p: ", p)
    print(bytesToStr(p, False))

    print("\nBrute Force: ")
    machine.bruteForce(x, c)
else:
    str = "10101010"
    # key = np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    key = "1010101010"
    key = strToBytes(key, True)
    # key = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], dtype=np.uint8)

    x = strToBytes(str, True)
    print(bytesToStr(x, True))
    print("p: ", x)

    machine = S_DES()
    c = machine.forward(x, key, isEncrypt=True)
    print("c: ", c)

    p = machine.forward(c, key, isEncrypt=False)
    print("p: ", p)
    print(bytesToStr(p, True))

    print("\nBrute Force: ")
    machine.bruteForce(x, c)

    print("随机暴力破解")
    pp = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
    cc = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8)
    machine.bruteForce(pp, cc)