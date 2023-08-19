#!/usr/bin/env python3

# type: ignore

import jwt

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoxNjkxOTUyNjU1NjcxLCJhZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwicm9sZSI6InVzZXIiLCJpYXQiOjE2OTE5NTI2NTZ9.ATTb_ka-l-NsRxYc7ggiy1XTwsT1_LRVFxMat6Z-YQU"

d = jwt.JWT.decode(token, options={"verify_signature": False})
print(d)
d['role'] = 'admin'
