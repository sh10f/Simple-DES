import time

import numpy as np

from utils import split, swap, merge, decToBin, binToDec, strToBytes, bytesToStr


class PBox:
    def __init__(self, in_length, out_order):
        # 设置该PBox的一些属性
        self.in_length = in_length
        self.out_order = out_order

    def cal(self, input):
        # 该PBox的计算
        result = input[self.out_order]
        return result


class SBox:
    def __init__(self, out_order):
        self.out_order = out_order

    def cal(self, input):
        row_index = [input[0], input[-1]]
        row = binToDec(row_index)

        column_index = input[1:-1]
        column = binToDec(column_index)

        result = self.out_order[row][column]
        result = decToBin(result)
        return result[-2:]


class KeyGenerator:
    def __init__(self):
        P10_order = np.array([3, 5, 2, 7, 4, 10, 1, 9, 8, 6]) - 1
        self.P10 = PBox(10, P10_order)

        P8_order = np.array([6, 3, 7, 4, 8, 5, 10, 9]) - 1
        self.P8 = PBox(8, P8_order)

        left1_order = np.array([2, 3, 4, 5, 1]) - 1
        self.LeftShift1 = PBox(5, left1_order)

        left2_order = np.array([3, 4, 5, 1, 2]) - 1
        self.LeftShift2 = PBox(5, left2_order)

    def cal(self, key):
        x = self.P10.cal(key)
        left, right = split(x)
        left, right = self.LeftShift1.cal(left), self.LeftShift1.cal(right)

        x = merge(left, right)
        k1 = self.P8.cal(x)

        left, right = self.LeftShift1.cal(left), self.LeftShift1.cal(right)
        x = merge(left, right)
        k2 = self.P8.cal(x)

        return k1, k2


class RoundFunction:
    def __init__(self):
        self.E_PBox_order = np.array([4, 1, 2, 3, 2, 3, 4, 1]) - 1
        self.E_PBox = PBox(4, self.E_PBox_order)

        SBox1_order = np.array([[1, 0, 3, 2],
                                [3, 2, 1, 0],
                                [0, 2, 1, 3],
                                [3, 1, 0, 2]])
        self.SBox1 = SBox(SBox1_order)

        SBox2_order = np.array([[0, 1, 2, 3],
                                [2, 3, 0, 1],
                                [3, 0, 1, 2],
                                [2, 1, 0, 3]])
        self.SBox2 = SBox(SBox2_order)

        self.S_PBox_order = np.array([2, 4, 3, 1]) - 1
        self.S_PBox = PBox(4, self.S_PBox_order)

    def cal(self, input, subkey):
        x = self.E_PBox.cal(input)

        x = x ^ subkey

        x_left, x_right = split(x)
        x_left = self.SBox1.cal(x_left)
        x_right = self.SBox2.cal(x_right)

        x = merge(x_left, x_right)
        x = self.S_PBox.cal(x)
        return x


class S_DES:
    def __init__(self):
        self.keyGenerator = KeyGenerator()

        IP_order = np.array([2, 6, 3, 1, 4, 8, 5, 7]) - 1
        self.IP = PBox(8, IP_order)

        LP_order = np.array([4, 1, 3, 5, 7, 2, 8, 6]) - 1
        self.LP = PBox(8, LP_order)

        self.roundF = RoundFunction()

    def forward(self, x, key, isEncrypt=True):
        """ 生成两个子密钥
        k1, k2 = keygenerator.cal()
        """
        if isEncrypt:
            k1, k2 = self.keyGenerator.cal(key)
        else:
            k2, k1 = self.keyGenerator.cal(key)
        tt = x.reshape((-1, 8))
        result = np.array([], dtype=np.uint8)
        for x in tt:
            x = self.IP.cal(x)
            left, right = split(x)
            left = left ^ self.roundF.cal(right, k1)
            left, right = swap(left, right)

            left = left ^ self.roundF.cal(right, k2)
            x = merge(left, right)
            x = self.LP.cal(x)
            result = np.append(result, x)
        return result

    def bruteForce(self, plaintext, ciphertext):
        keys = np.array([], dtype=np.uint8)

        time_start = time.process_time()
        for i in range(pow(2, 10)):
            i_str = np.binary_repr(i, width=10)
            key = strToBytes(i_str, True)
            ciphertext_DES = self.forward(plaintext, key, True)
            if np.sum(ciphertext_DES == ciphertext) == ciphertext.shape[0]:
                keys = np.append(keys, key)
                print(key, " --- {}".format(i))
        time_end = time.process_time()
        print("Brute Force spend: ", 1000*(time_end - time_start), " ms")

        keys = keys.reshape(-1, 10)
        time_spend = 1000 * (time_end - time_start)
        print(keys)

        return keys, time_spend


if __name__ == '__main__':
    test = True
    if test:

        str = "你好！ -- -- Hello!"
        key = np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
        x = strToBytes(str, False)
        print(bytesToStr(x, False))
        print("p: ", x)

        machine = S_DES()
        c = machine.forward(x, key, isEncrypt=True)
        print("c: ", c)

        p = machine.forward(c, key, isEncrypt=False)
        print("p: ", p)
        print(bytesToStr(p, False))
        print("Brute Force: \n")
        machine.bruteForce(x, c)
    else:
        str = "11100011"
        # key = np.array([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
        key = np.array([1, 1, 1, 0, 0, 0, 0, 0, 1, 0])

        x = strToBytes(str, True)
        print(bytesToStr(x, True))
        print("p: ", x)

        machine = S_DES()
        c = machine.forward(x, key, isEncrypt=True)
        print("c: ", c)

        p = machine.forward(c, key, isEncrypt=False)
        print("p: ", p)
        print(bytesToStr(p, True))

