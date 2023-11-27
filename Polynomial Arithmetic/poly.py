from flask import Flask, request, render_template, jsonify
import numpy.polynomial.polynomial as P
import numpy
from polynomial_arithmetic import *
app = Flask(__name__)
app.static_folder = 'static'

# Your polynomial class, State class, and other functions go here

@app.route("/", methods=['GET'])
def main():
    return render_template('index1.html')

@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        # Get data from the frontend
        operation = request.json['operation']
        mValue = int(request.json['mValue'])
        poly1 = request.json.get('poly1', '')
        poly2 = request.json.get('poly2', '')
        # Convert user input to hexadecimal format
        poly1_hex = int(poly1, 2) if poly1.startswith('0b') else int(poly1, 16)
        if (operation != 'modulo' and operation != 'inverse'):
            poly2_hex = int(poly2, 2) if poly2.startswith('0b') else int(poly2, 16)
        mod = polynomial(0x95) # Assume we have the mod in GF(2^m())
        # Perform the selected operation (add more cases as needed)
        if operation == 'add':
            result = polynomial(poly1_hex, mValue) + polynomial(poly2_hex, mValue)
        elif operation == 'subtract':
            result = polynomial(poly1_hex, mValue) - polynomial(poly2_hex, mValue)
        elif operation == 'multiply':
            result = polynomial(poly1_hex, mValue) * polynomial(poly2_hex, mValue)
        elif operation == 'divide':
            result = polynomial(poly1_hex, mValue) / polynomial(poly2_hex, mValue)
        elif operation == 'inverse':
            try:
                result = extendedgcdPoly(mod,polynomial(poly1_hex, mValue),mod)[1]
            except Exception as e :
                print(e)
            states_html = [state.toHTMLHex() for state in STATES]
            return jsonify({'result': str(result), 'steps': states_html})
        elif operation == 'modulo':
            result = polynomial(poly1_hex, mValue)%mod
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        # Return the result to the frontend
        return jsonify({'result': str(result)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
