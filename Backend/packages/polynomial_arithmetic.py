import numpy.polynomial.polynomial as P
import numpy


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
                    <td colspan="2">{}</td>
                    <td colspan="2">{}</td>
                    <td colspan="3">{}</td>
                </tr>
                <tr>
                    <td colspan="2">{}</td>
                    <td colspan="2">{}</td>
                    <td colspan="3">{}</td>
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


class Tasks:
    def task1():
        return


if __name__ == "__main__":
    a = polynomial(0x11B)
    b = polynomial(0x95)
    # print(a.toHex())
    with open("out.html", "w") as f:
        extendedgcdPoly(a, b, a)
        for i in range(len(STATES)):
            STATES[i] = STATES[i].toHTMLHex()
            f.write(STATES[i])
        print(STATES)


"""
For generating irreducible polynomials.
https://sagecell.sagemath.org/
sage: R = GF(2)['x']
sage: for p in R.polynomials(163):
....:     if p.is_irreducible():
....:         print(p)
"""

"""x^163 + x^18 + x^17 + x^15 + x^14 + x^12 + x^9 + x^7 + x^6 + x^5 + x^4 + x + 1"""
