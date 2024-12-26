#!/usr/bin/env python3

import json
import time

import httpx


class Client:
    def __init__(self, url) -> None:
        self.url = httpx.URL(url)
        self.start_time = int(time.time())
        self.headers = {"User-Agent": "okhttp/4.12.0"}
        self.session = httpx.Client(
            proxy="http://172.29.32.1:8080", verify=False, headers=self.headers
        )
        self.end_time = self.start_time
        self.game_id = None
        self.eqs = []

    def urljoin(self, path) -> httpx.URL:
        return self.url.join(path)

    def start(self) -> None:
        data = {"start_time": self.start_time}
        res = self.session.post(self.urljoin("/start"), json=data)
        if res.status_code == 200:
            out = json.loads(res.text)
            self.game_id = out["game_id"]
            self.eqs = out["equations"]
        else:
            print("error /start")
            print(res.text)
            quit()

    def submit(self) -> None:
        data = {
            "game_id": self.game_id,
            "end_time": self.end_time,
        }
        res = self.session.post(self.urljoin("/submit"), json=data)
        if res.status_code == 200:
            print(res.text)
        else:
            print("error /submit")
            print(res.text)
            quit()

    def solve(self) -> None:
        for eq in self.eqs:
            self.end_time += int(eval(eq))


c = Client("https://quiz.ctf.intigriti.io")
c.start()
c.solve()
c.submit()
