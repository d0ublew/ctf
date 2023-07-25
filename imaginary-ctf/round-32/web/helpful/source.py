#!/usr/bin/env python3

from sqlite3 import *

from random import choice
from hashlib import sha512

from flask import Flask, request, Response, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

salt = b'very_secure_salt'

class PassHash(str):
    def __str__(self):
        return sha512(salt + self.encode()).hexdigest()

    def __repr__(self):
        return sha512(salt + self.encode()).hexdigest()

con = connect("users.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("CREATE TABLE users(username, passhash)")
passhash = PassHash(''.join(choice("0123456789") for i in range(7)))
cur.execute(
    "INSERT INTO users VALUES (?, ?)",
    ("admin", str(passhash))
)
con.commit()

@app.route('/source')
@limiter.limit("5/second")
def source():
    return Response(open(__file__).read(), mimetype="text/plain")

@app.route('/')
@limiter.limit("2/second")
def index():
    if 'username' not in request.args or 'password' not in request.args:
        return open("index.html").read()
    else:
        username = request.args["username"]
        new_pwd = PassHash(request.args["password"])
        con = connect("users.db")
        cur = con.cursor()
        res = cur.execute(
            "SELECT * from users WHERE username = ? AND passhash = ?",
            (username, str(new_pwd))
        )
        if res.fetchone():
            return open("flag.txt").read()
        return ("Sorry, we couldn't find a user '{user}' with password hash <code>{{passhash}}</code>!"
            .format(user=username)
            .format(passhash=new_pwd)
        )

if __name__ == "__main__":
    app.run('0.0.0.0', 11005)
