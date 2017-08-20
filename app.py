from flask import Flask, request, render_template

from route import Route
from route.db import init_db, db_session

import os


app = Flask(__name__)
app.debug = False

# Secret Key setting based on debug setting
if app.debug:
    app.secret_key = "T3st_s3cret_k3y!~$@"
else:
    init_db()
    app.secret_key = os.urandom(30)


@app.teardown_request
def remove_session(exception=None):
    db_session.remove()


@app.route("/domain", methods=["GET", "POST"])
def domain():
    ip = request.form.get("ip")
    domain = request.form.get("domain")
    
    if (ip and domain) is None:
        return "parameter error", 400

    r = Route(ip, domain)
    
    if request.method == "GET":
        # search domain
        rows = r.search()

    elif request.method == "POST":
        # register domain
        owner = request.form.get("owner")

        if owner is not None:
            r.register(owner)
        else:
            return "owner not found", 400

    del r

    return "success", 200


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
