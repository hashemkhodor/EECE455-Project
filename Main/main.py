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
    return render_template("main.html")


@app.route("/about", methods=["GET", "POST"])
def About():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
