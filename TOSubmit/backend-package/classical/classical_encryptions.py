import string

##################################### Affine Cipher #####################################################################
LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters
# LETTERS = "".join([chr(ord('A')+i) for i in range(26)])


class Affine:
    LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters
    # LETTERS = "".join([chr(ord('A')+i) for i in range(26)])

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


##################################### Vigenere Cipher #####################################################################

LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters


# LETTERS = "".join([chr(ord('a')+i) for i in range(26)])
# print(LETTERS)
class Vigenere:
    LETTERS = "".join(str(i) for i in range(10)) + string.ascii_letters
    # LETTERS = "".join([chr(ord('a')+i) for i in range(26)])
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
        # print(KEYS)
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
                index = (index + 1) % len(self.key)
            else:
                LIST.append(" ")
        return "".join(LIST)

    def encrypt(self, text):
        EXTENDED_KEY = self._get_vigenere_string_(text)
        return "".join(list(map(self.TRANSFORM_ENC, text, EXTENDED_KEY)))

    def decrypt(self, text):
        EXTENDED_KEY = self._get_vigenere_string_(text)
        return "".join(list(map(self.TRANSFORM_DEC, text, EXTENDED_KEY)))


def encrypt_affine_cipher(message, a, b, operation):
    affine_obj = Affine(a, b)
    if operation:
        encrypted_message = affine_obj.encrypt(message)

        return encrypted_message
    else:
        decrypted_message = affine_obj.decrypt(message)
        return decrypted_message


def encrypt_vigenere_cipher(message, key, operation):
    vigenere_obj = Vigenere(key)
    if operation:
        encrypted_message = vigenere_obj.encrypt(message)
        return encrypted_message
    else:
        decrypted_message = vigenere_obj.decrypt(message)
        return decrypted_message


def find_modular_inverse(a, m):
    x1, x2, x3 = extended_gcd(m, a)
    return x3
