#!/usr/bin/env python3

"""
Dragon Cafe Login Microservice | Author: Sam Griffith | Org: Alta3 Research Inc.

This Login Microservice is the second part of the monolithic application of a Chinese Restaurant website that has been broken out into it's own service.
"""

from aiohttp import web
import jinja2
from pathlib import Path
import random
import requests
import socket
import os

HOST = os.getenv("LOGIN_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("LOGIN_PORT", 2228)
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
            web.get("/", login),
            web.get("/login", login),
            web.post("/logging_in", logging_in),
            web.post("/login/logging_in", logging_in),
        ]
    )


async def logging_in(request):
    """
    This is the page that gets POSTED to to allow a user to login
    """
    print(request)
    if request.method == 'POST':
        data = await request.post()
        name = data['name']
        print("POSTED")
        print(name)
        # TODO - Add authentication logic
        get_login = await login(request, name=name)
        return get_login


async def login(request, name=None):
    """
    This is the login page for the website
    """
    print(request)
    if name is not None:
        page = Page(filename="hello.html", args={"name": name})
        print("Cookies Set?")
        return page.render()
    else:
        print("No name has been sent yet!")
        args = {"name": name}
        page = Page(filename="login.html", args=args)
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