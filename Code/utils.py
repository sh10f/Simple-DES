import numpy as np


def split(input):
    length = input.shape[0]
    mid = length // 2
    return input[:mid], input[mid:]


def swap(left, right):
    return right, left


def merge(left, right):
    result = left
    result = np.append(result, right)
    return result


def binToDec(input):
    binary_string = ''.join(np.array(input).astype(str))

    # 使用 int 函数将二进制字符串转换为十进制
    decimal_value = int(binary_string, 2)
    return decimal_value


def decToBin(input):
    t = np.array(input, dtype=np.uint8)
    binary_array = np.unpackbits(t)
    return binary_array


def strToBytes(strings, isBinary=True):
    if isBinary:
        binary_array = np.array([ord(char) - 48 for char in strings], dtype=np.uint8)
    else:
        t = strings.encode('utf-8')
        t = np.array([i for i in t], dtype=np.uint8)
        binary_array = np.unpackbits(t)
        print(binary_array.shape)

    return binary_array


def bytesToStr(binary_array, isBinary=True):
    if isBinary:
        string_result = str(binary_array).strip("[]").replace(" ", "")

    else:
        # 将二进制数组重塑为字节数组
        byte_array = np.packbits(binary_array)

        # 将字节数组转换为字符串
        string_result = byte_array.tobytes().decode('utf-8', errors='ignore')
    return string_result




if __name__ == '__main__':
    a = np.array([1, 1, 0, 0])
    b = np.array([0, 1, 0, 1])

    print(merge(a, b))
