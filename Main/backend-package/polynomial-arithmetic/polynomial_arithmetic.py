import numpy.polynomial.polynomial as P
import numpy


import os
import json

isMAC = False  # If you are macos , set it to True
delimeter = "\\"
if isMAC:
    delimeter = "/"

PATH = os.path.abspath(__file__)
PATH = PATH.split(delimeter)[:-1]
PATH = "/".join(PATH)

POLYNOMIALS = json.loads(
    open(
        "{}/POLY.txt".format(PATH),
        "r",
    ).read()
)


class polynomial:
    def __init__(self, coeff, mod=2):
        assert type(coeff) in (list, int, numpy.ndarray), "Invalid Type"
        if type(coeff) == int:
            # In this case, the user inputed the coeff in hexadecimal format
            # 0x23542ac -> 00100011....
            __coeff__ = list(map(int, list(bin(coeff))[2:]))
            __coeff__.reverse()
        else:
            __coeff__ = coeff

        self.polynomial = P.Polynomial(P.polytrim(__coeff__))
        self.polynomial.coef %= 2

    def __add__(self, other):
        """ """
        assert type(other) == polynomial, "Invalid Type"
        res = self.polynomial + other.polynomial
        res = P.polytrim(res.coef % 2)
        return polynomial(res, 2)

    def __sub__(self, other):
        """ """
        assert type(other) == polynomial, "Invalid Type"
        return self.__add__(other)

    def __mul__(self, other):
        """"""
        assert type(other) == polynomial, "Invalid Type"
        res = ((self.polynomial * other.polynomial)).coef % 2
        return polynomial(P.polytrim(res), 2)

    def __truediv__(self, other):
        assert type(other) == polynomial, "Invalid Type"
        res = (self.polynomial // other.polynomial).coef % 2
        return polynomial(P.polytrim(res), 2)
        # return super().__truediv__(other)

    def __mod__(self, other):
        assert type(other) == polynomial, "Invalid Type"
        res = (self.polynomial % other.polynomial).coef % 2
        return polynomial(res, 2)

    def __str__(self):
        return self.polynomial.__str__()

    def __eq__(self, other):
        assert type(other) == polynomial, "Invalid Type"
        return self.polynomial.__eq__(other.polynomial)

    def toHex(self):
        return hex(
            int(
                "0b{}".format(
                    "".join(map(str, map(int, reversed(self.polynomial.coef))))
                ),
                2,
            )
        )


class State:
    """
    Used to represent state captured by the extended gcd algorithm.
    The state consists of :
    a = r11*x + r12*y
    b = r21*x + r22*y
    Q = a//b
    The above are to be filled in the outputed table.
    content = {
                'r11': polynomial(),
                'r12': polynomial(),
                'a'  : polynomial(),
                'r21': polynomial(),
                'r22': polynomial(),
                'b'  : polynomial(),
                'Q'  : polynomial(), // Quotient
    }
    """

    def __init__(self, content):
        assert all(
            [
                x in content
                and (
                    type(content[x]) == polynomial
                    if x != "Q"
                    else type(content[x]) in (polynomial, str)
                )
                for x in ("r11", "r12", "r21", "r22", "a", "b", "Q")
            ]
        ), "Invalid Content"
        self.__content__ = content

    def toHTMLHex(self):
        skeleton = """<tr>
                    <td colspan="2" rowspan="2">{}</td>
                    <td colspan="2" class="result-text ">{}</td>
                    <td colspan="2" class="result-text ">{}</td>
                    <td colspan="3" class="result-text ">{}</td>
                </tr>
                <tr>
                    <td colspan="2" class="result-text ">{}</td>
                    <td colspan="2" class="result-text ">{}</td>
                    <td colspan="3" class="result-text ">{}</td>
                </tr>""".format(
            self.__content__["Q"]
            if type(self.__content__["Q"]) == str
            else self.__content__["Q"].toHex(),
            self.__content__["r11"].toHex(),
            self.__content__["r12"].toHex(),
            self.__content__["a"].toHex(),
            self.__content__["r21"].toHex(),
            self.__content__["r22"].toHex(),
            self.__content__["b"].toHex(),
        )
        return skeleton

    def toHTMLStr(self):
        skeleton = """<tr>
                    <td colspan="2" rowspan="2">{}</td>
                    <td colspan="2">{}</td>
                    <td colspan="2">{}</td>
                    <td colspan="3">{}</td>
                </tr>
                <tr>
                    <td colspan="2">{}</td>
                    <td colspan="2">{}</td>
                    <td colspan="3">{}</td>
                </tr>""".format(
            self.__content__["Q"],
            str(self.__content__["r11"]),
            str(self.__content__["r12"]),
            str(self.__content__["a"]),
            str(self.__content__["r21"]),
            str(self.__content__["r22"]),
            str(self.__content__["b"]),
        )
        return skeleton

    def toHTMLHex2(self, step_number):
        if step_number == 1:
            # Initialization step
            skeleton = """<tr>
                             <td colspan="2">Initialization: A1(x) = {}, A2(x) = {}, A3(x) = {}, B1(x) = {}, B2(x) = {}, B3(x) = {} </td>
                         </tr>""".format(
                self.__content__["r11"].toHex(),
                self.__content__["r12"].toHex(),
                self.__content__["a"].toHex(),
                self.__content__["r21"].toHex(),
                self.__content__["r22"].toHex(),
                self.__content__["b"].toHex(),
            )
        else:
            # Iteration step
            skeleton = """<tr>
                             <td colspan="2">Step {}: Q(x) = {}, A1(x) = {}, A2(x) = {}, A3(x) = {}, B1(x) = {}, B2(x) = {}, B3(x) = {}</td>
                         </tr>""".format(
                step_number,
                self.__content__["Q"].toHex(),
                self.__content__["r11"].toHex(),
                self.__content__["r12"].toHex(),
                self.__content__["a"].toHex(),
                self.__content__["r21"].toHex(),
                self.__content__["r22"].toHex(),
                self.__content__["b"].toHex(),
            )
        return skeleton

    def toHTMLStr2(self, step_number):
        if step_number == 1:
            # Initialization step
            skeleton = """<tr>
                             <td>{}, {},  {}, {},  {}, {}</td>
                           </tr>""".format(
                str(self.__content__["r11"]),
                str(self.__content__["r12"]),
                str(self.__content__["a"]),
                str(self.__content__["r21"]),
                str(self.__content__["r22"]),
                str(self.__content__["b"]),
            )
        else:
            # Iteration step
            skeleton = """<tr>
                             <td>{}</td>
                             <td>{}, {}, {},  {}, {}, {}</td>
                           </tr>""".format(
                step_number,
                str(self.__content__["Q"]),
                str(self.__content__["r11"]),
                str(self.__content__["r12"]),
                str(self.__content__["a"]),
                str(self.__content__["r21"]),
                str(self.__content__["r22"]),
                str(self.__content__["b"]),
            )
        return skeleton


STATES = []


def extendedgcdPoly(a, b, MOD):
    STATES.clear()
    r11, r12 = polynomial(0x0), polynomial(0x0)
    r21, r22 = polynomial(0x1), polynomial(0x0)
    r31, r32 = polynomial(0x0), polynomial(0x1)
    factor = "Initialization"
    while sum(b.polynomial.coef) != 0:
        r11, r12 = r21, r22
        r21, r22 = r31, r32
        STATES.append(
            State(
                {
                    "Q": factor,
                    "r11": r11,
                    "r12": r12,
                    "r21": r21,
                    "r22": r22,
                    "a": a,
                    "b": b,
                }
            )
        )
        factor = a / b

        r31 = (r11 - factor * r21) % MOD
        r32 = (r12 - factor * r22) % MOD
        a, b = b, a % b

    return a, r21, r22


class CLEAN:
    def clean(POWER: int, operation: str, input1: str, input2: str):
        try:
            POWER = int(POWER)
        except:
            pass

        VALID_HEX = (
            [chr(ord("0") + i) for i in range(10)]
            + [chr(ord("a") + i) for i in range(6)]
            + [chr(ord("A") + i) for i in range(6)]
        )
        VALID_BIN = ["0", "1"]
        RESULT = {
            "m_error": "",
            "m_success": "",
            "operation_error": "",
            "operation_success": "",
            "input1_error": "",
            "input2_error": "",
            "input1_success": "",
            "input2_success": "",
        }
        ################## Validated Power == m ##########################
        if type(POWER) != int:
            RESULT[
                "m_error"
            ] = "Expected integer m instead of {} which is of type {}".format(
                POWER, type(POWER)
            )

        elif POWER > 2000:
            RESULT[
                "m_error"
            ] = "Please change your m ({}) to another value less than 2000".format(
                POWER
            )

        if RESULT["m_error"] == "":
            RESULT["m_success"] = "Irreducible polynomial of GF(2^{}) = {}".format(
                POWER, POLYNOMIALS[str(POWER)]
            )
            RESULT["irr_poly"] = polynomial(int(POLYNOMIALS[str(POWER)], 16))
            RESULT["m"] = POWER

        ##################################################################

        ################## Validate operation ############################
        if operation not in [
            "inverse",
            "modulo",
            "addition",
            "subtraction",
            "multiplication",
            "division",
            "inverse_bin",
        ]:
            RESULT["operation_error"] = "Invalid operation"
        else:
            RESULT["operation_success"] = " "
            RESULT["operation"] = operation

        ##################################################################

        ################## Validate input1    ############################
        if input1 == None or len(input1) < 2:
            RESULT["input1_error"] = "Invalid : empty input"

        elif input1[:2] not in ("0b", "0x"):
            RESULT[
                "input1_error"
            ] = "Invalid: expected to start with 0b for binary or 0x for hexadecimal"

        elif input1[:2] == "0b":
            IS_BIN = lambda x: x in VALID_BIN
            if not all(map(IS_BIN, input1[2:])):
                RESULT[
                    "input1_error"
                ] = "Invalid : expected all the characters to be either '0' or '1' "
            elif RESULT["input1_error"] == "":
                coeff = list(map(int, input1[2:]))
                coeff.reverse()
                # if polynomial(coeff) / RESULT["irr_poly"] != polynomial(0x0):
                #     RESULT[
                #         "input1_error"
                #     ] == "Invalid polynomial, expected to be less than {}".format(
                #         RESULT["irr_poly"].toHex()
                #     )
                # else:
                RESULT["input1_success"] = "The polynomial of {} is {}".format(
                    input1, polynomial(coeff)
                )
                RESULT["input1"] = polynomial(coeff)

        elif input1[:2] == "0x":
            IS_HEX = lambda x: x in VALID_HEX
            if not all(map(IS_HEX, input1[2:])):
                RESULT[
                    "input1_error"
                ] = "Invalid : expected all the characters to be between 0-9 and (a-f or A-F) "
            elif RESULT["input1_error"] == "":
                # if polynomial(int(input2, 16)) / RESULT["irr_poly"] != polynomial(0x0):
                #     RESULT[
                #         "input1_error"
                #     ] = "Invalid polynomial, expected to be less than {}".format(
                #         RESULT["irr_poly"].toHex()
                #     )
                # else:
                RESULT["input1_success"] = "The polynomial of {} is {}".format(
                    input1, polynomial(int(input1, 16))
                )
                RESULT["input1"] = polynomial(int(input1, 16))

        ##################################################################

        ################## Validate input2    ############################
        if operation == "inverse":
            pass
        elif (input2 == None or len(input2) < 2) and operation != "inverse":
            RESULT["input2_error"] = "Invalid : empty input"
        elif input2[:2] not in ("0b", "0x"):
            RESULT[
                "input2_error"
            ] = "Invalid: expected to start with 0b for binary or 0x for hexadecimal"

        elif input2[:2] == "0b":
            IS_BIN = lambda x: x in VALID_BIN
            if not all(map(IS_BIN, input2[2:])):
                RESULT[
                    "input2_error"
                ] = "Invalid : expected all the characters to be either '0' or '1' "
            elif RESULT["input2_error"] == "":
                coeff = list(map(int, input2[2:]))
                coeff.reverse()
                # if polynomial(coeff) / RESULT["irr_poly"] != polynomial(0x0):
                #     RESULT[
                #         "input2_error"
                #     ] = "Invalid polynomial, expected to be less than {}".format(
                #         RESULT["irr_poly"].toHex()
                #     )
                # else:
                RESULT["input2_success"] = "The polynomial of {} is {}".format(
                    input2, polynomial(coeff)
                )
                RESULT["input2"] = polynomial(coeff)

        elif input2[:2] == "0x":
            IS_HEX = lambda x: x in VALID_HEX
            if not all(map(IS_HEX, input2[2:])):
                RESULT[
                    "input2_error"
                ] = "Invalid : expected all the characters to be between 0-9 and (a-f or A-F) "
            elif RESULT["input2_error"] == "":
                # if polynomial(int(input2, 16)) / RESULT["irr_poly"] != polynomial(0x0):
                #     RESULT[
                #         "input2_error"
                #     ] = "Invalid polynomial, expected to be less than {}".format(
                #         RESULT["irr_poly"].toHex()
                #     )
                # else:
                RESULT["input2_success"] = "The polynomial of {} is {}".format(
                    input2, polynomial(int(input2, 16))
                )
                RESULT["input2"] = polynomial(int(input2, 16))

        ##################################################################

        return RESULT
