from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.static_folder = "static"


@app.route("/", ["GET"])
def _main_():
    return render_template()


@app.route("/AES", ["GET", "POST"])
def _main_():
    return render_template()


@app.route("/DES", ["GET", "POST"])
def _main_():
    return render_template()


@app.route("/classical", ["GET", "POST"])
def _main_():
    return render_template()


@app.route("/polynomial-arithmetic", ["GET", "POST"])
def _main_():
    return render_template()


@app.route("/about", ["GET", "POST"])
def _main_():
    return render_template()
