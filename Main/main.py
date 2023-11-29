from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.static_folder = "static"


@app.route("/", ["GET"])
def _main_():
    return render_template()
