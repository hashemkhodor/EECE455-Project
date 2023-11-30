from flask import Flask, request, render_template, jsonify

import sys
import os


##################### Added By HK ####################################################
# Used to specify the directories of the ciphers.
BACKEND_PACKAGES = ["AES", "DES", "classical", "polynomial-arithmetic"]
for BACKEND_PACKAGE in BACKEND_PACKAGES:
    sys.path.append(
        os.path.join(os.path.dirname(__file__), "backend-package", BACKEND_PACKAGE)
    )

######################################################################################
app = Flask(__name__)
app.static_folder = "static"


print(sys.path)
##################### CONFIGURATION SECTION ###################################
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
        "{}/backend-package/polynomial-arithmetic/POLY.txt".format(PATH),
        "r",
    ).read()
)

# GET POLYNOMIALS

##################### CONFIGURATION SECTION ###################################


@app.route("/", methods=["GET", "POST"])
def MAIN():
    return render_template("main.html")


@app.route("/AES", methods=["GET", "POST"])
def AES():
    import AES

    ciphertext = ""
    result1 = []
    result2 = []

    if request.method == "POST":
        plaintext = int(request.form.get("plain"), 16)
        # hex_value = hex(p)[2:]
        # plaintext="0x" + "0" * (len(hex_value) % 2) + hex_value

        print(plaintext)

        # k = int(request.form.get('key'),16)
        # hex_value = hex(k)[2:]
        # key="0x" + "0" * (len(hex_value) % 2) + hex_value
        key = int(request.form.get("key"), 16)

        c = AES.AES(key)
        rrr, keywords, aux = c.expand_key(key)
        (
            ciphertext,
            startOfRound,
            afterSubBytes,
            afterShiftRows,
            afterMixColumns,
            roundKey,
        ) = c.encrypt(plaintext)
        result1 = [(x, y) for x, y in zip(keywords, aux)]
        result2 = [
            (x, y, z, w, n)
            for x, y, z, w, n in zip(
                startOfRound, afterSubBytes, afterShiftRows, afterMixColumns, roundKey
            )
        ]
        print(len(result2))

    return render_template(
        "./AES/AES.html", ciphertext=ciphertext, result1=result1, result2=result2
    )


@app.route("/DES", methods=["GET", "POST"])
def DES():
    import DES_code

    result = []
    proc = ""
    r = ""
    if request.method == "POST":
        if "encrypt" in request.form:
            p = int(request.form.get("plain"), 16)
            plaintext = str(bin(p))[2:]
            plaintext = "0" * (64 - len(plaintext)) + plaintext

            k = int(request.form.get("key"), 16)

            key = str(bin(k))[2:]
            key = "0" * (64 - len(key)) + key
            keys, L, R = DES_code.DES(plaintext, key)
            rounds = [
                "IP",
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                "IP-1",
            ]
            result = [(x, y, z, w) for x, y, z, w in zip(rounds, keys, L, R)]
            proc = "Encryption"
            r = str(L[17]) + str(R[17])

        else:
            p = int(request.form.get("plain"), 16)

            plaintext = str(bin(p))[2:]
            plaintext = "0" * (64 - len(plaintext)) + plaintext
            k = int(request.form.get("key"), 16)
            key = str(bin(k))[2:]
            key = "0" * (64 - len(key)) + key
            keys, L, R = DES_code.DES_DECRYPT(plaintext, key)
            rounds = [
                "IP",
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                "IP-1",
            ]
            result = [(x, y, z, w) for x, y, z, w in zip(rounds, keys, L, R)]
            proc = "Decryption"
            r = str(L[17]) + str(R[17])

    return render_template("./DES/DES.html", result=result, proc=proc, r=r)


######################### CLASSICAL ##################################################################################
from classical_encryptions import (
    find_modular_inverse,
    encrypt_vigenere_cipher,
    encrypt_affine_cipher,
)


@app.route("/classical")
def index():
    # This function will render the 'index.html' template
    # and pass some data to be displayed in the HTML.
    return render_template("./classical/page.html")


@app.route("/classical/encrypt", methods=["GET", "POST"])
def encrypt():
    result = None
    a = int(request.form["integer"])
    m = int(request.form["modulus"])
    active_form = "extendedEuclideanForm"  # Set the active form to determine when to display the result
    result = find_modular_inverse(a, m)
    return render_template(
        "./classical/page.html", result=result, active_form=active_form
    )


@app.route("/classical/encrypt2", methods=["GET", "POST"])
def encrypt2():
    key = request.form["vigenereKey"]
    message = request.form["vigenereMessage"]
    operation = request.form["vigenereOperation"]
    active_form = "vignere"

    if operation == "encrypt":
        result = encrypt_vigenere_cipher(message, key, 1)
    elif operation == "decrypt":
        result = encrypt_vigenere_cipher(message, key, 0)
    else:
        result = "Invalid operation"

    return render_template(
        "./classical/page.html", result=result, active_form=active_form
    )


@app.route("/classical/encrypt3", methods=["POST"])
def encrypt3():
    a = int(request.form["a"])
    b = int(request.form["b"])
    message = request.form["message"]
    operation = request.form["operation"]
    active_form = "affine"

    if operation == "encrypt":
        result = encrypt_affine_cipher(message, a, b, 1)

    elif operation == "decrypt":
        result = encrypt_affine_cipher(message, a, b, 0)
    else:
        result = "Invalid operation"

    return render_template(
        "./classical/page.html", result=result, active_form=active_form
    )


########################################################################################################################
from polynomial_arithmetic import polynomial, extendedgcdPoly, STATES, State


class Polynomial_Handler:
    def handle_inverse(RESULT):
        """returns dictonary"""
        GCD, inv1, inv2 = extendedgcdPoly(
            RESULT["input1"], RESULT["irr_poly"], RESULT["irr_poly"]
        )
        RESULT["result"] = ""
        for state in STATES:
            print(state.toHTMLHex())
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


@app.route("/polynomial-arithmetic", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        m = request.form.get("m")
        if m:
            operation = request.form.get("operation")
            input1 = request.form.get("input1")
            input2 = request.form.get("input2")

            RESULT = CLEAN.clean(m, operation, input1, input2)
            if "input1" not in RESULT:
                RESULT["input1"] = input1
            if "input2" not in RESULT:
                RESULT["input2"] = input2
            if not RESULT["input2"]:
                RESULT["input2"] = ""
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
                "./polynomial/index3.html",
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
                    else RESULT["result"].toHex()
                ),
                result_success=RESULT["result_success"],
                result_error=RESULT["result_error"],
                input1=(
                    RESULT["input1"]
                    if type(RESULT["input1"]) in (str, None)
                    else RESULT["input1"].toHex()
                ),
                input2=(
                    RESULT["input2"]
                    if type(RESULT["input2"]) in (str, None)
                    else RESULT["input2"].toHex()
                ),
                # input2=RESULT["input2"],
                op=RESULT["op"],
                input1_raw=RESULT["input1_raw"],
                input2_raw=RESULT["input2_raw"],
            )
    return render_template(
        "./polynomial/index3.html", operation=request.form.get("operation")
    )


###################################################################################################################################################


@app.route("/about", methods=["GET", "POST"])
def About():
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)
