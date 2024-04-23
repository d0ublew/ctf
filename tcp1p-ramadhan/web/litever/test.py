#!/usr/bin/env python3

import sqlite3

db = "d0ublew.sqlite"
conn = sqlite3.connect(db)

cur = conn.cursor()
cur.execute("PRAGMA database_list")
r = cur.fetchall()
print(r)
cur.close()

cur = conn.cursor()
cur.execute("SELECT * FROM users WHERE a=(ATTACH DATABASE 'flag.sqlite' as pog)")
r = cur.fetchall()
print(r)
cur.close()

cur = conn.cursor()
cur.execute("PRAGMA database_list")
r = cur.fetchall()
print(r)
cur.close()

conn.close()
