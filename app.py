from flask import Flask, request, render_template
from route import Route

import os


app = Flask(__name__)
app.debug = False

# Secret Key setting based on debug setting
if app.debug:
    app.secret_key = "T3st_s3cret_k3y!~$@"
else:
    app.secret_key = os.urandom(30)


@app.route("/domain", methods=["GET", "POST"])
def domain():
    if request.method == "GET":
        # search domain
        pass

    elif request.method == "POST":
        # register domain
        pass


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
