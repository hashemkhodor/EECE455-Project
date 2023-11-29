"""
1 - Extendended euclid
2 - Hill Cipher
3 - Playfair Cipher
4 - Vigenere Cipher
5 - Mono-Alphabetic Cipher 
6 - Affine Cipher  
"""
import numpy as np


##################################### Extended Euclid #################################################################
def extended_gcd(a, b):
    c11, c12 = 0, 0
    c21, c22 = 1, 0
    c31, c32 = 0, 1
    while a % b != 0:
        c11, c12 = c21, c22
        c21, c22 = c31, c32
        k = a // b
        c31, c32 = c11 - k * c21, c12 - k * c22
        tmp = a
        a = b
        b = tmp % a
    return abs(b), c31, c32


#######################################################################################################################

##################################### Hill Cipher #####################################################################


class HillCipher:
    def __init__(self, key):
        assert (
            type(key) in (list, tuple) and len(key) == 2 and len(key[0]) == 2
        ), "Invalid Key Format : Expected 2x2 matrix"
        for i in range(2):
            for j in range(2):
                assert (
                    type(key[i][j]) == int
                ), f"Invalid element in the key : expected int type instead of {type(key[i][j])}"
        self.__key__ = np.matrix(key)
        gcd, k1, k2 = extended_gcd(int(np.linalg.det(self.__key__)), 26)
        assert gcd == 1, "Invalid key : it's determinant may not be invertible mod 26"
        self.__detinverse__ = k1

    def encrypt(self, plaintext):
        if len(plaintext) % 2 == 1:
            plaintext += "X"  # fillers
        i = 0
        cipherText = []
        while i + 1 < len(plaintext):
            x, y = plaintext[i], plaintext[i + 1]
            column = np.matrix([[ord(x) - ord("A")], [ord(y) - ord("A")]])
            res = (self.__key__ * column) % 26
            cipherText.append(chr(res[0, 0] + ord("A")))
            cipherText.append(chr(res[1, 0] + ord("A")))
            i += 2
        return "".join(cipherText)

    def decrypt(self, ciphertext):
        i = 0
        cipherText = []
        invMatrix = np.matrix(
            [
                [self.__key__[1, 1], -self.__key__[0, 1]],
                [-self.__key__[1, 0], self.__key__[0, 0]],
            ]
        )
        # print(invMatrix)
        while i + 1 < len(ciphertext):
            x, y = ciphertext[i], ciphertext[i + 1]
            column = np.matrix([[ord(x) - ord("A")], [ord(y) - ord("A")]])
            res = (self.__detinverse__ * invMatrix * column) % 26
            # print(res)
            cipherText.append(chr(res[0, 0] + ord("A")))
            cipherText.append(chr(res[1, 0] + ord("A")))
            i += 2
        return "".join(cipherText)


#######################################################################################################################


##################################### Playfair Cipher #####################################################################
import string
import numpy as np


class Playfair:
    def __init__(self, key):
        L = []
        S = set()
        MAP = lambda x: x if x not in ("I", "J") else "I"
        for char in key:
            if MAP(char) not in S:
                L.append(MAP(char))
                S.add(MAP(char))
        for char in string.ascii_uppercase:
            if MAP(char) not in S:
                L.append(MAP(char))
                S.add(MAP(char))

        self.__key__ = [[0 for i in range(5)] for j in range(5)]
        self.__dic__ = {}
        for i in range(len(L)):
            self.__key__[i // 5][i % 5] = L[i]
            self.__dic__[L[i]] = (i // 5, i % 5)

    def __encrypt(self, plaintext, toAdd):
        UpdatedText = []
        MAP = lambda x: x if x not in ("I", "J") else "I"
        for i in range(len(plaintext)):
            UpdatedText.append(MAP(plaintext[i]))
            if i + 1 < len(plaintext) and MAP(plaintext[i]) == MAP(plaintext[i + 1]):
                UpdatedText.append("X")
        if len(UpdatedText) % 2 == 1:
            UpdatedText.append("X")
        CipherText = []
        i = 0
        while i + 1 < len(UpdatedText):
            x, y = UpdatedText[i], UpdatedText[i + 1]
            if self.__dic__[x][0] == self.__dic__[y][0]:
                new_x, new_y = (
                    self.__key__[self.__dic__[x][0]][(self.__dic__[x][1] + toAdd) % 5],
                    self.__key__[self.__dic__[y][0]][(self.__dic__[y][1] + toAdd) % 5],
                )
            elif self.__dic__[x][1] == self.__dic__[y][1]:
                new_x, new_y = (
                    self.__key__[(self.__dic__[x][0] + toAdd) % 5][self.__dic__[x][1]],
                    self.__key__[(self.__dic__[y][0] + toAdd) % 5][self.__dic__[y][1]],
                )
            else:
                new_x, new_y = (
                    self.__key__[self.__dic__[x][0]][self.__dic__[y][1]],
                    self.__key__[self.__dic__[y][0]][self.__dic__[x][1]],
                )
            CipherText.append(new_x)
            CipherText.append(new_y)
            i += 2

        return "".join(CipherText)

    def encrypt(self, plaintext):
        return self.__encrypt(plaintext, 1)

    def decrypt(self, ciphertext):
        return self.__encrypt(ciphertext, -1)


###########################################################################################################################


##################################### Vigenere Cipher #####################################################################

LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters


class Vigenere:
    LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters
    KEYS = dict([(LETTERS[i], i) for i in range(len(LETTERS))])

    def __init__(self, key):
        ## Assert type(key) == string
        assert (
            type(key) == str
        ), "INVALID KEY: Expected type string instead of {}".format(type(key))
        assert len(key) > 0, "Empty key"
        ## Assert each character in the string is inside the Keys dictionary (valid alphabet)
        for char in key:
            assert (
                char in Vigenere.KEYS
            ), "INVALID character : {} is not inside our alphabet".format(char)

        self.key = key
        self.__mod__ = len(Vigenere.LETTERS)
        self.SHIFT_ENC = lambda c, a: (c + a) % self.__mod__
        self.SHIFT_DEC = lambda c, a: (c - a + self.__mod__) % self.__mod__
        self.TRANSFORM_ENC = (
            lambda x, y: x
            if x not in Vigenere.KEYS
            else Vigenere.LETTERS[self.SHIFT_ENC(Vigenere.KEYS[x], Vigenere.KEYS[y])]
        )
        self.TRANSFORM_DEC = (
            lambda x, y: x
            if x not in Vigenere.KEYS
            else Vigenere.LETTERS[self.SHIFT_DEC(Vigenere.KEYS[x], Vigenere.KEYS[y])]
        )

    def _get_vigenere_string_(self, text):
        """Returns string which is the key ignoring the spaces and new lines"""
        index = 0
        LIST = []
        for i in range(len(text)):
            if text[i] in Vigenere.KEYS:
                LIST.append(self.key[index])
                index = (index + 1) % self.__mod__
            else:
                LIST.append(" ")
        return "".join(LIST)

    def encrypt(self, text):
        EXTENDED_KEY = self._get_vigenere_string_(text)

        return "".join(list(map(self.TRANSFORM_ENC, text, EXTENDED_KEY)))

    def decrypt(self, text):
        EXTENDED_KEY = self._get_vigenere_string_(text)
        return "".join(list(map(self.TRANSFORM_DEC, text, EXTENDED_KEY)))


###########################################################################################################################


##################################### Affine Cipher #####################################################################
import string

LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters


class Affine:
    LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters
    KEYS = dict([(LETTERS[i], i) for i in range(len(LETTERS))])

    def __init__(self, a, b):
        assert (type(a), type(b)) == (
            int,
            int,
        ), "INVALID TYPES : Expected type(a)=int and type(b) = int instead of type(a) = {} and type(b) = {}".format(
            type(a), type(b)
        )
        assert a < len(Affine.KEYS), "Expected a < {}".format(len(Affine.KEYS))
        assert b < len(Affine.KEYS), "Expected b < {}".format(len(Affine.KEYS))
        mod = len(Affine.KEYS)
        GCD, inv1, inv2 = extended_gcd(mod, a)
        assert GCD == 1, "Expected gcd(a,{}) = 1 ; Got a gcd(a,{}) = {}".format(
            mod, mod, GCD
        )
        self.__a__ = a
        self.__b__ = b
        self.__mod__ = mod
        self.__ainv__ = inv2
        self.SHIFT_ENC = lambda c: (self.__a__ * c + self.__b__) % self.__mod__
        self.SHIFT_DEC = lambda c: (self.__ainv__ * (c - self.__b__)) % self.__mod__
        self.TRANSFORM_ENC = (
            lambda x: x
            if x not in Affine.KEYS
            else Affine.LETTERS[self.SHIFT_ENC(Affine.KEYS[x])]
        )
        self.TRANSFORM_DEC = (
            lambda x: x
            if x not in Affine.KEYS
            else Affine.LETTERS[self.SHIFT_DEC(Affine.KEYS[x])]
        )

    def encrypt(self, text):
        return "".join(list(map(self.TRANSFORM_ENC, text)))

    def decrypt(self, text):
        return "".join(list(map(self.TRANSFORM_DEC, text)))


###########################################################################################################################


if __name__ == "__main__":
    import string

    B = Vigenere("hashemWhatisWRONGwithyou12023")
    TEXT = "I want to get her back okay !I Want &@*$@!#)@#$(@$)!#(@!#(!@$(@!(#!@($)))))"
    CIPHERTEXT = B.encrypt(TEXT)
    PLAINTEXT = B.decrypt(CIPHERTEXT)
    print(CIPHERTEXT)
    print(PLAINTEXT)

    D = Playfair("IWNRAIDASD")
    TEXT = "HH"
    CIPHERTEXT = D.encrypt(TEXT)
    PLAINTEXT = D.decrypt(CIPHERTEXT)
    print(CIPHERTEXT)
    print(PLAINTEXT)
