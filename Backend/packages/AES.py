"""
################################### ARCHITECTURE ###############################################################

format_text(text:128 bits) -> 4x4 byte matrix
class AES:
    key: 128 bits
    + encrypt(plaintext :128 bits) -> 128 bits
    + decrypt(ciphertext:128 bits) -> 128 bits
    + add_round_key(text:4x4 byte matrix, key:4x4 byte matrix) -> 4x4 bytes matrix
    + expand_key(key: 128 bits)-> array of size 10 of 4x4 byte matrix
    + substitute_bytes(text:4x4 byte matrix) -> 4x4 byte matrix
    + shift_rows(text:4x4 byte matrix) -> 4x4 byte matrix
    + mix_columns(text:4x4 byte matrix) -> 4x4 byte matrix

class polynomial:
    coeff: array 
    mod  : polynomial 
    
predefined tables:
s_box table:
substitute_bytes_table = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16],
]



"""
from AES_tables import *
from polynomial_arithmetic import polynomial


def transpose(M):
    RES = [[-1 for i in range(len(M))] for j in range(len(M[0]))]
    for j in range(len(M[0])):
        for i in range(len(M)):
            RES[j][i] = M[i][j]
    return RES


def intTOHEX(M: list[list[int]]):
    _M_Formated_ = [
        [
            "{}".format(
                "0" + hex(element)[2:] if len(hex(element)) == 3 else hex(element)[2:]
            )
            for element in row
        ]
        for row in M
    ]
    return "\n" + "\n".join([" ".join(x) for x in _M_Formated_]) + "\n"


def matrix_mult(A, B, mod):
    result = [[polynomial(0) for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            if type(A[i][j]) != polynomial:
                A[i][j] = polynomial(A[i][j])
    # Perform matrix multiplication
    # print(result)
    for i in range(len(A)):
        for j in range(len(B[0])):
            # print(i, j)
            for k in range(len(B)):
                # print(result[i][j])
                # print(A[i])
                result[i][j] = (result[i][j] + (A[i][k] * B[k][j])) % mod
            result[i][j] = int(result[i][j].toHex(), 16)

    return result


def bits_to_matrix(text):
    # print(text)
    text = "0" * (34 - len(hex(text))) + hex(text)[2:]
    # print(text)

    out = [[0 for i in range(4)] for j in range(4)]
    index = 0
    for col in range(4):
        for row in range(4):
            # print("0x" + text[index : index + 2])
            out[row][col] = int("0x" + text[index : index + 2], 16)
            index += 2

    return out


def SubWord(text):
    text = hex(text)[2:]
    text = "0" * (8 - len(text)) + text
    Groups = [text[i : i + 2] for i in range(0, len(text) - 1, 2)]
    # print(Groups)
    out = []
    for group in Groups:
        row, col = int(f"0x{group[0]}", 16), int(f"0x{group[1]}", 16)
        SUB = substitute_bytes_table[row][col]
        SUB = hex(SUB)[2:]
        SUB = "0" * (2 - len(SUB)) + SUB
        out.append(SUB)

    return int("0x" + "".join(out), 16)


def RotWord(text):
    text = hex(text)[2:]
    text = "0" * (8 - len(text)) + text
    text = text[2:] + text[:2]
    return int("0x" + text, 16)


def printMatrix(matrix):
    import numpy as np

    new_matrix = [[element for element in row] for row in matrix]
    for row in range(len(new_matrix)):
        for col in range(len(new_matrix[row])):
            new_matrix[row][col] = hex(new_matrix[row][col])
    print(np.matrix(new_matrix))


class AES:
    def __init__(self, key):
        assert type(key) == int, "Invalid Type"
        fix = lambda x: "0" * (10 - len(hex(x))) + hex(x)[2:]
        self.__keys__ = []
        temp_keys = self.expand_key(key)

        for i in range(0, len(temp_keys), 4):
            keys = list(map(fix, temp_keys[i : i + 4]))

            self.__keys__.append(bits_to_matrix(int("0x" + "".join(keys), 16)))
        # self.__key__ = self.expand_key(key)

    def expand_key(self, key):
        """

        Parameters
        ----------
        Return
        -------
        """
        new_key = hex(key)[2:]
        if len(new_key) != 32:
            new_key = "0" * (32 - len(new_key)) + new_key
        w = ["" for i in range(44)]
        new_key = [new_key[i : i + 2] for i in range(0, len(new_key) - 1, 2)]
        for i in range(4):
            w[i] = int(
                "0x"
                + new_key[4 * i]
                + new_key[4 * i + 1]
                + new_key[4 * i + 2]
                + new_key[4 * i + 3],
                16,
            )
            # [
            #     int("0x" + new_key[4 * i], 16),
            #     int("0x" + new_key[4 * i + 1], 16),
            #     int("0x" + new_key[4 * i + 2], 16),
            #     int("0x" + new_key[4 * i + 3], 16),
            # ]
            print(f"w{i} = {'0'*(10-len(hex(w[i])))+hex(w[i])[2:]}")

        for i in range(4, 44):
            temp = w[i - 1]
            if i % 4 == 0:
                print(i // 4)
                temp = RotWord(temp)
                print(f"RotWord(w{i-1}) = {'0'*(10-len(hex(temp)))+hex(temp)[2:]}")
                temp = SubWord(temp)
                print(f"SubWord(w{i-1}) = {'0'*(10-len(hex(temp)))+hex(temp)[2:]}")
                print(
                    f"RCON({i//4}) = {'0'*(10-len(hex(RC_table[i // 4])))+hex(RC_table[i // 4])[2:]}"
                )
                temp = temp ^ RC_table[i // 4]
                print(
                    f"y{i//4} xor Rcon({i//4}) = {'0'*(10-len(hex(temp)))+hex(temp)[2:]}"
                )
                # print(hex(temp))
                print("")
                # temp = SubWord(RotWord(temp)) ^ RC_table[i // 4]

            w[i] = temp ^ w[i - 4]

            if i % 4 == 3:
                for j in range(4):
                    print(f"w{i-j}=", hex(w[i - j]))
        print(w)
        return w

    def add_round_key(self, text_formatted, key):
        new_text = [
            [
                element if type(element) == int else int(element[2:], 16)
                for element in row
            ]
            for row in text_formatted
        ]
        for row in range(len(new_text)):
            for col in range(len(new_text[row])):
                new_text[row][col] ^= key[row][col]

        return new_text

    def substitute_bytes(self, text):
        new_text = [[element for element in row] for row in text]
        for row in range(len(new_text)):
            for col in range(len(new_text[row])):
                new_row, new_col = (
                    new_text[row][col] >> 4 & 0xF,
                    new_text[row][col] & 0xF,
                )
                new_text[row][col] = substitute_bytes_table[new_row][new_col]
        return new_text

    def shift_rows(self, text):
        new_text = [[element for element in row] for row in text]
        for row in range(0, len(new_text)):
            for col in range(len(new_text[row])):
                new_text[row][col] = text[row][(col + row) % len(new_text[row])]
        return new_text

    def mix_columns(self, text):
        new_text = [[polynomial(element) for element in row] for row in text]
        new_mix_columns_table = [
            [polynomial(element) for element in row] for row in mix_columns_table
        ]
        MOD = polynomial(0x11B)
        return matrix_mult(new_mix_columns_table, new_text, MOD)
        # return

    def encrypt(self, plaintext):
        import numpy as np

        plaintext_formatted = bits_to_matrix(plaintext)
        print(intTOHEX(plaintext_formatted))
        plaintext_formatted = self.add_round_key(plaintext_formatted, self.__keys__[0])
        for i in range(1, 11):
            print("##############{}###############".format(i))
            print(intTOHEX(plaintext_formatted))

            plaintext_formatted = self.substitute_bytes(plaintext_formatted)
            print(intTOHEX(plaintext_formatted))
            plaintext_formatted = self.shift_rows(plaintext_formatted)
            print(intTOHEX(plaintext_formatted))
            if i != 10:
                plaintext_formatted = self.mix_columns(plaintext_formatted)
                print(intTOHEX(plaintext_formatted))
            plaintext_formatted = self.add_round_key(
                plaintext_formatted, self.__keys__[i]
            )
            print(intTOHEX(self.__keys__[i]))
            print("##############################")
        print(intTOHEX(plaintext_formatted))
        return plaintext_formatted


if __name__ == "__main__":
    import numpy as np

    Hashem = AES(0x0F1571C947D9E8590CB7ADD6AF7F6798)
    TEXT = 0x0123456789ABCDEFFEDCBA9876543210
    print(intTOHEX(Hashem.encrypt(TEXT)))

    # # Hashem = AES(0x20202020202020202020202020202020)
    # Hashem = AES(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
    # # Hashem = AES(0x0F1571C947D9E8590CB7ADD6AF7F6798)
    # A = [
    #     [0xEA, 0x04, 0x65, 0x85],
    #     [0x83, 0x45, 0x5D, 0x96],
    #     [0x5C, 0x33, 0x98, 0xB0],
    #     [0xF0, 0x2D, 0xAD, 0xC5],
    # ]
    # B = [
    #     [0x87, 0xF2, 0x4D, 0x97],
    #     [0xEC, 0x6E, 0x4C, 0x90],
    #     [0x4A, 0xC3, 0x46, 0xE7],
    #     [0x8C, 0xD8, 0x95, 0xA6],
    # ]
    # # print(np.matrix(Hashem.substitute_bytes(A)))
    # # print(np.matrix(Hashem.shift_rows(B)))
    # print("################ PROBLEM 1 #########################")

    # print("################ PROBLEM 2 #########################")
    # # key = 0x0F1571C947D9E8590CB7ADD6AF7F6798
    # key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    # # print(bits_to_matrix(0xFFFFFFFFFFACFFFFFFFFFFFFFFFFFFFFF))
    # # print(hex(RotWord(0x7F8D292F)))
    # # print(hex(SubWord(0x8D292F7F)))
    # keys = Hashem.expand_key(key)
    # # print(keys)
    # for i in range(len(keys)):
    #     keys[i] = hex(keys[i])
    # # print(Hashem.expand_key(key))
    # print(keys)
    # print("################ PROBLEM 3 #########################")
    # plaintext = 0x000102030405060708090A0B0C0D0E0F
    # key = 0x20202020202020202020202020202020
    # # Hashem = AES(key)
    # Hashem.encrypt(plaintext)

    # print("################ PROBLEM 4 #########################")
    # MOD = polynomial(0x11B)
    # ROW = [[polynomial(0x2), polynomial(0x3), polynomial(0x1), polynomial(0x1)]]
    # COL = [
    #     [polynomial(0x87)],
    #     [polynomial(0x6E)],
    #     [polynomial(0x46)],
    #     [polynomial(0xA6)],
    # ]
    # COL = [
    #     [polynomial(0x55)],
    #     [polynomial(0x43)],
    #     [polynomial(0x93)],
    #     [polynomial(0x07)],
    # ]
    # # ROW = list(map(polynomial, ROW))
    # # COL = list(map(polynomial, COL))
    # printMatrix(matrix_mult(mix_columns_table, COL, MOD))

    # # print(((polynomial(0x02) * polynomial(0x87)) % MOD).to_hex())
    # # Hashem.substitute_bytes([[1, 2, 3], [4, 5, 6]])
