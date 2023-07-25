#!/usr/bin/env python3

from hashlib import sha512

salt = b'very_secure_salt'


class PassHash(str):
    def __str__(self):
        return sha512(salt + self.encode()).hexdigest()

    def __repr__(self):
        return sha512(salt + self.encode()).hexdigest()


def main(username, new_pwd):
    return ("Sorry, we couldn't find a user '{user}' with password hash <code>{{passhash}}</code>!"
            .format(user=username)
            .format(passhash=new_pwd)
            )
