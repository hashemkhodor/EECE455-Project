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


@app.route("/classical", methods=["GET", "POST"])
def classical():
    return render_template("main.html")


@app.route("/polynomial-arithmetic", methods=["GET", "POST"])
def Poly_Arith():
    from polynomial_arithmetic import polynomial, extendedgcdPoly, STATES, State

    try:
        # Get data from the frontend
        operation = request.json["operation"]
        mValue = int(request.json["mValue"])
        poly1 = request.json.get("poly1", "")
        poly2 = request.json.get("poly2", "")
        result = 0
        ######## Checking
        if poly1.startswith("0b"):
            for j in range(2, len(poly1)):
                if poly1[j] != "1" and poly1[j] != "0":
                    raise ValueError("Invalid Format : Must be 0s and 1s only")
        else:
            for c in poly1:
                if not (ord("0") <= ord(c) and ord(c) <= ord("F")) and not (
                    (ord("a") <= ord(c) and ord(c) <= ord("f"))
                ):
                    raise ValueError("Invalud Format : Must be in Hexadecimal Format")
        ########
        # Convert user input to hexadecimal format
        poly1_hex = int(poly1, 2) if poly1.startswith("0b") else int(poly1, 16)

        if mValue > 1000:
            raise ValueError("Our website supports mods up to 1000")

        mod = int(POLYNOMIALS.get(str(mValue), ""), 16)

        if operation != "modulo" and operation != "inverse":
            if poly2.startswith("0b"):
                for j in range(2, len(poly2)):
                    if poly2[j] != "1" and poly2[j] != "0":
                        raise ValueError("Invalid Format : Must be 0s and 1s only")
            else:
                for c in poly2:
                    if not (ord("0") <= ord(c) and ord(c) <= ord("F")) and not (
                        (ord("a") <= ord(c) and ord(c) <= ord("f"))
                    ):
                        raise ValueError(
                            "Invalud Format : Must be in Hexadecimal Format"
                        )
            poly2_hex = int(poly2, 2) if poly2.startswith("0b") else int(poly2, 16)

        if operation == "add":
            result = polynomial(poly1_hex) + polynomial(poly2_hex)
        elif operation == "subtract":
            result = polynomial(poly1_hex) - polynomial(poly2_hex)
        elif operation == "multiply":
            result = polynomial(poly1_hex) * polynomial(poly2_hex)
        elif operation == "divide":
            result = polynomial(poly1_hex) / polynomial(poly2_hex)
        elif operation == "inverse":
            result = extendedgcdPoly(
                polynomial(mod), polynomial(poly1_hex), polynomial(mod)
            )[1]
            states_html = [state.toHTMLHex() for state in STATES]
            print(states_html)
            return jsonify({"result": str(result), "steps": states_html})
        elif operation == "modulo":
            result = polynomial(poly1_hex) % polynomial(mod)
        else:
            return jsonify({"error": "Invalid operation"}), 400

        # Return the result to the frontend
        return jsonify({"result": str(result)})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/about", methods=["GET", "POST"])
def About():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
