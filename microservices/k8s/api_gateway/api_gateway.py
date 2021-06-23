#!/usr/bin/env python3

"""
Dragon Cafe Microservices API Gateway

Author: Sam Griffith | Org: Alta3 Research Inc.

This is the primary microservice that users from the "outside" will connect to
in order to access the microservices within.
"""

from aiohttp import web
import jinja2
from pathlib import Path
import random
import requests
import socket
import os
import json

HOST = os.getenv("API_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("API_PORT", 2225)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
REG_PORT = os.getenv("SR_PORT", 55555)
SERVICE = os.path.basename(__file__).rstrip(".py")

class Page:
    def __init__(self, filename, templates_dir=Path("templates"), args={}, cookies={}):
        """
        Create a new instance of an html page to be returned
        :param filename: name of file found in the templates_dir
        """
        self.path = templates_dir
        self.file = templates_dir / filename
        self.args = args
        self.cookies = cookies

    def render(self):
        with open(self.file) as f:
            txt = f.read()
            print(f"Templating in {self.args}")
            j2 = jinja2.Template(txt).render(self.args)
            resp = web.Response(text=j2, content_type='text/html')
            for c, j in self.cookies:
                resp.set_cookie(c, j)
            return resp


def routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/", home),
            web.get("/{service_name}", service),
            web.get("/{service_name}/{ex_path}", service),
            web.post("/{service_name}/{ex_path}", service),
        ]
    )


async def service(request) -> web.Response:
    print(request)
    svc_name = request.match_info.get('service_name', '')
    ex_path = request.match_info.get('ex_path', '')
    svc_host = requests.get(f"http://{REG_ADDR}:{REG_PORT}/get_one/{svc_name}").text
    svc_host = json.loads(svc_host)
    svc_ip = svc_host["endpoints"][0]
    svc_port = svc_host["endpoints"][1]
    if request.method == "POST":
        data = await request.post()
        r = requests.post(f"http://{svc_ip}:{svc_port}/{ex_path}", data=data)
    else:
        r = requests.get(f"http://{svc_ip}:{svc_port}/{ex_path}")
    return web.Response(text=r.text, content_type='text/html')


async def home(request) -> web.Response:
    """
    This is the home page for the website
    """
    print(request)
    page = Page(filename="index.html")
    return page.render()


def main():
    """
    This is the main process for the aiohttp server.

    This works by instantiating the app as a web.Application(),
    then applying the setup function we built in our routes
    function to add routes to our app, then by starting the async
    event loop with web.run_app().
    """

    print("This aiohttp web server is starting up!")
    app = web.Application()
    routes(app)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
