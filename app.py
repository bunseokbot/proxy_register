from flask import Flask

import os


app = Flask(__name__)
app.debug = True

# Secret Key setting based on debug setting
if app.debug:
    app.secret_key = "T3st_s3cret_k3y!~$@"
else:
    app.secret_key = os.urandom(30)


@app.route("/")
def index():
    return "Index Page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)