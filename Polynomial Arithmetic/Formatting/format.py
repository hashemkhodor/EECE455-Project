import os

A = "1285 : x^1285 + x^9 + x^7 + x^5 + x^3 + x^2 + 1"


def SPLIT1(TEXT):
    POWER, CONTENT = TEXT.split(" : ")
    CONTENT = CONTENT.split(" + ")
    for i in range(len(CONTENT)):
        CONTENT[i] = CONTENT[i].split("^")[-1]
        if CONTENT[i] == "x":
            CONTENT[i] = 1
        elif CONTENT[i] == "1":
            CONTENT[i] = 0
        else:
            CONTENT[i] = int(CONTENT[i])

    return CONTENT


def MAIN_SPLIT(TEXT):
    POLYNOMIALS = TEXT.split("\n")
    for i in range(len(POLYNOMIALS)):
        POLYNOMIALS[i] = SPLIT1(POLYNOMIALS[i])
        print(POLYNOMIALS[i])
    return POLYNOMIALS


def get_hex(coeff: list[int]):
    OUTPUT = ["0" for i in range(coeff[0] + 1)]
    for x in coeff:
        OUTPUT[x] = "1"
    OUTPUT.reverse()
    return hex(int("".join(OUTPUT), 2))


import json


def format(inFile, outFile=""):
    assert os.path.isfile(inFile), "FILE {} doesn't exist".format(inFile)
    with open(inFile, "r") as F:
        TEXT = F.read()
        F.close()

    CONTENT = MAIN_SPLIT(TEXT)
    RESULT = dict()
    for content in CONTENT:
        RESULT[content[0]] = get_hex(content)
    with open(outFile, "w") as F:
        F.write(json.dumps(RESULT))
        F.close()
    return True
    # print(CONTENT)


format(
    "./Polynomial Arithmetic/Formatting/output.txt",
    "./Polynomial Arithmetic/Formatting/POLY.txt",
)
