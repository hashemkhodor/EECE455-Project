from flask import Flask, request, render_template, jsonify

# import numpy.polynomial.polynomial as P
# import numpy
from polynomial_arithmetic import *

app = Flask(__name__)
app.static_folder = "static"

################################# Updated by HK################################################################
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
# print(POLYNOMIALS)
###############################################################################################################
# Your polynomial class, State class, and other functions go here

#  0b
#  0x
## SO it takes by name.


def SANITIZE(POWER: int, operation: str, input1: str, input2: str):
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
        ] = "Please change your m ({}) to another value less than 2000".format(POWER)

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


class Polynomial_Handler:
    def handle_inverse(RESULT):
        """returns dictonary"""
        GCD, inv1, inv2 = extendedgcdPoly(
            RESULT["input1"], RESULT["irr_poly"], RESULT["irr_poly"]
        )
        RESULT["result"] = ""
        for state in STATES:
            RESULT["result"] += state.toHTMLHex()

    def handle_inverse_bin(RESULT):
        """returns dictonary"""
        if RESULT["input2"] == polynomial(0x0):
            RESULT["result_error"] = ""
            RESULT["input2_error"] = "Division by Zero is not allowed"
            RESULT["input2_success"] = ""

            return

        GCD, inv1, inv2 = extendedgcdPoly(
            RESULT["input1"], RESULT["input2"], RESULT["irr_poly"]
        )
        RESULT["result"] = ""
        for state in STATES:
            print(state)
            RESULT["result"] += state.toHTMLHex()

        return

    def handle_addition(RESULT):
        RESULT["op"] = "+"
        RESULT["result"] = (RESULT["input1"] + RESULT["input2"]) % RESULT["irr_poly"]

    def handle_multplication(RESULT):
        RESULT["op"] = "*"
        RESULT["result"] = (RESULT["input1"] * RESULT["input2"]) % RESULT["irr_poly"]

    def handle_division(RESULT):
        # Handle zero division
        RESULT["op"] = "/"
        if RESULT["input2"] == polynomial(0x0):
            RESULT["result_error"] = ""
            RESULT["input2_error"] = "Division by Zero is not allowed"
            RESULT["input2_success"] = ""
        else:
            RESULT["result"] = (RESULT["input1"] / RESULT["input2"]) % RESULT[
                "irr_poly"
            ]

    def handle_mod(RESULT):
        RESULT["op"] = "%"
        print(RESULT["input2"])
        if RESULT["input2"] == polynomial(0x0):
            RESULT["result_error"] = ""
            RESULT["input2_error"] = "Modulo Zero is not allowed"
            RESULT["input2_success"] = ""
        else:
            RESULT["result"] = (RESULT["input1"] % RESULT["input2"]) % RESULT[
                "irr_poly"
            ]

    def handle_subtraction(RESULT):
        RESULT["op"] = "-"
        RESULT["result"] = (RESULT["input1"] - RESULT["input2"]) % RESULT["irr_poly"]


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        m = request.form.get("m")
        if m:
            operation = request.form.get("operation")
            input1 = request.form.get("input1")
            input2 = request.form.get("input2")

            RESULT = SANITIZE(m, operation, input1, input2)
            if "input1" not in RESULT:
                RESULT["input1"] = input1
            if "input2" not in RESULT:
                RESULT["input2"] = input2
            RESULT["result"] = ""
            RESULT["result_error"] = ""
            RESULT["result_success"] = ""
            RESULT["op"] = ""
            RESULT["input2_raw"] = input2
            RESULT["input1_raw"] = input1

            print(operation)
            if (
                not RESULT["m_success"]
                or not RESULT["input1_success"]
                or (not RESULT["input2_success"] and operation != "inverse")
                or not RESULT["operation_success"]
            ):
                print("DEAL")
                pass
            elif operation == "inverse":
                print("DEAL")
                Polynomial_Handler.handle_inverse(RESULT)
            elif operation == "modulo":
                Polynomial_Handler.handle_mod(RESULT)
            elif operation == "addition":
                Polynomial_Handler.handle_addition(RESULT)
            elif operation == "subtraction":
                Polynomial_Handler.handle_subtraction(RESULT)
            elif operation == "multiplication":
                Polynomial_Handler.handle_multplication(RESULT)
            elif operation == "division":
                Polynomial_Handler.handle_division(RESULT)
            elif operation == "inverse_bin":
                Polynomial_Handler.handle_inverse_bin(RESULT)
            else:
                pass

            return render_template(
                "index3.html",
                m=m,
                operation=operation,
                m_error=RESULT["m_error"],
                m_success=RESULT["m_success"],
                operation_success=RESULT["operation_success"],
                operation_error=RESULT["operation_error"],
                input1_error=RESULT["input1_error"],
                input1_success=RESULT["input1_success"],
                input2_error=RESULT["input2_error"],
                input2_success=RESULT["input2_success"],
                result=(
                    RESULT["result"]
                    if type(RESULT["result"]) == str
                    else RESULT["result"]
                ),
                result_success=RESULT["result_success"],
                result_error=RESULT["result_error"],
                input1=RESULT["input1"],
                input2=RESULT["input2"],
                op=RESULT["op"],
                input1_raw=RESULT["input1_raw"],
                input2_raw=RESULT["input2_raw"],
            )
    return render_template("index3.html", operation=request.form.get("operation"))


@app.route("/calculate", methods=["POST"])
def calculate():
    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True)
