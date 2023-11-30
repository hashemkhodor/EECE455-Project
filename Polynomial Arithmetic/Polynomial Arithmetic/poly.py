from flask import Flask, request, render_template, jsonify
import numpy.polynomial.polynomial as P
import numpy
from polynomial_arithmetic import *

app = Flask(__name__)
app.static_folder = "static"

################################# Updated by HK################################################################
import os
import json

isMAC=True #If you are macos , set it to True
delimeter="\\"
if isMAC:
    delimeter="/"

PATH = os.path.abspath(__file__)
PATH = PATH.split(delimeter)[:-1]
PATH = "/".join(PATH)

POLYNOMIALS = json.loads(
    open(
        "POLY.txt".format(PATH),
        "r",
    ).read()
)
print(POLYNOMIALS)
###############################################################################################################
# Your polynomial class, State class, and other functions go here


@app.route("/", methods=["GET"])
def main():
    return render_template("index1.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        # Get data from the frontend
        operation = request.json["operation"]
        mValue = int(request.json["mValue"])
        poly1 = request.json.get("poly1", "")
        poly2 = request.json.get("poly2", "")
        result = 0
        ######## Checking
        if poly1.startswith("0b"):
            for j in range(2,len(poly1)):
                if poly1[j] != '1' and poly1[j] != '0':
                    raise ValueError("Invalid Format : Must be 0s and 1s only")
        else:
            for c in poly1 : 
                
                if not (ord('0') <= ord(c) and ord(c) <= ord('F')) and not ((ord('a') <= ord(c) and ord(c) <= ord('f'))):
                    raise ValueError("Invalud Format : Must be in Hexadecimal Format")
        ########
        # Convert user input to hexadecimal format
        poly1_hex = int(poly1, 2) if poly1.startswith("0b") else int(poly1, 16)

        if mValue > 1000:
            raise ValueError("Our website supports mods up to 1000")
        
        mod = int(POLYNOMIALS.get(str(mValue), ""), 16)
        
                        
        if operation != "modulo" and operation != "inverse":
            if poly2.startswith("0b"):
                for j in range(2,len(poly2)):
                    if poly2[j] != '1' and poly2[j] != '0':
                        raise ValueError("Invalid Format : Must be 0s and 1s only")
            else:
                for c in poly2 : 
                    if not (ord('0') <= ord(c) and ord(c) <= ord('F')) and not ((ord('a') <= ord(c) and ord(c) <= ord('f'))):
                        raise ValueError("Invalud Format : Must be in Hexadecimal Format")
            poly2_hex = int(poly2, 2) if poly2.startswith("0b") else int(poly2, 16)
            

        if operation == "add":
            result = polynomial(poly1_hex) + polynomial(poly2_hex)
        elif operation == "subtract":
            result = polynomial(poly1_hex) - polynomial(poly2_hex)
        elif operation == "multiply":
            result = polynomial(poly1_hex) * polynomial(poly2_hex)
        elif operation == "divide":
            result = polynomial(poly1_hex) / polynomial(poly2_hex)
        elif operation == 'inverse':
            result = extendedgcdPoly(polynomial(mod), polynomial(poly1_hex), polynomial(mod))[1]
            states_html = [state.toHTMLHex() for i, state in enumerate(STATES)]
            print(states_html)
            return jsonify({'result': str(result), 'steps': states_html})
        elif operation == 'modulo':
            result = polynomial(poly1_hex) % polynomial(mod)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        # Return the result to the frontend
        return jsonify({"result": str(result)})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
