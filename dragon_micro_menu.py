#!/usr/bin/env python3

"""
Dragon Cafe Monolithic Application with Menu Microservice | Author: Sam Griffith | Org: Alta3 Research Inc.

This monolithic application is a Chinese Restaurant website,
with the addition of the menu microservice.
"""

from aiohttp import web
import jinja2
from pathlib import Path
import random
import os
import requests
import socket
import json

HOST = os.getenv("DRAGON_HOST", "0.0.0.0")
LOCAL_IP = socket.gethostbyname(socket.gethostname())
PORT = os.getenv("DRAGON_PORT", 2225)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
REG_PORT = os.getenv("SR_PORT", 55555)
SERVICE = __file__.rstrip(".py")


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
            web.get("/login", login),
            web.post("/logging_in", logging_in),
            web.get("/closed_cookie", closed_cookie),
            web.get("/fortune_cookie", fortune_cookie),
            web.get("/menu", menu),
            web.get("/v2/menu", menu_v2),
        ]
    )


async def menu_v2(request) -> web.Response:
    print(request)
    menu_svc = requests.get(f"http://{REG_ADDR}:{REG_PORT}/get_one/menu").text
    print(menu_svc)
    menu_host = json.loads(menu_svc)
    menu_ip = menu_host['endpoints'][0]
    menu_port = menu_host['endpoints'][1]
    r = requests.get(f"http://{menu_ip}:{menu_port}/menu")
    return web.Response(text=r.text, content_type='text/html')


async def home(request) -> web.Response:
    """
    This is the home page for the website
    """
    page = Page(filename="index.html")
    return page.render()


async def logging_in(request):
    print(f"logging_in: {request}")
    if request.method == 'POST':
        data = await request.post()
        name = data['name']
        print("POSTED")
        print(name)
        # TODO - Add authentication logic
        poodle = await login(request, name=name)
        return poodle


async def login(request, name=None):
    """
    This is the login page for the website
    """
    print(f"login: {request}")
    # if request.query.get('name') is not None:
    if name is not None:
        print("We got something here!")
        # TODO - Add authentication logic
        resp = web.Response(text=name)
        page = Page(filename="hello.html", args={"name": name})
        print("Cookies Set?")
        return page.render()
    else:
        print("No name has been sent yet!")
        args = {"name": name}
        page = Page(filename="login.html", args=args)
        return page.render()


async def closed_cookie(request) -> web.Response:
    """
    This is the primary landing page for the fortune service.
    """
    page = Page(filename="cookie.html")
    return page.render()


async def fortune_cookie(request) -> web.Response:
    """
    This is the primary landing page for the fortune service.
    """

    possible = [
        "People are naturally attracted to you.",
        "You learn from your mistakes... You will learn a lot today.",
        "If you have something good in your life, don't let it go!",
        "What ever you're goal is in life, embrace it visualize it, and for it will be yours.",
        "Your shoes will make you happy today.",
        "You cannot love life until you live the life you love.",
        "Be on the lookout for coming events; They cast their shadows beforehand.",
        "Land is always on the mind of a flying bird.",
        "The man or woman you desire feels the same about you.",
        "Meeting adversity well is the source of your strength.",
        "A dream you have will come true.",
        "Our deeds determine us, as much as we determine our deeds.",
        "Never give up. You're not a failure if you don't give up.",
        "You will become great if you believe in yourself.",
        "There is no greater pleasure than seeing your loved ones prosper.",
        "You will marry your lover.",
        "A very attractive person has a message for you.",
        "You already know the answer to the questions lingering inside your head.",
        "It is now, and in this world, that we must live.",
        "You must try, or hate yourself for not trying.",
        "You can make your own happiness.",
        "The greatest risk is not taking one.",
        "The love of your life is stepping into your planet this summer.",
        "Love can last a lifetime, if you want it to.",
        "Adversity is the parent of virtue.",
        "Serious trouble will bypass you.",
        "A short stranger will soon enter your life with blessings to share.",
        "Now is the time to try something new.",
        "Wealth awaits you very soon.",
        "If you feel you are right, stand firmly by your convictions.",
        "If winter comes, can spring be far behind?",
        "Keep your eye out for someone special.",
        "You are very talented in many ways.",
        "A stranger, is a friend you have not spoken to yet.",
        "A new voyage will fill your life with untold memories.",
        "You will travel to many exotic places in your lifetime.",
        "Your ability for accomplishment will follow with success.",
        "Nothing astonishes men so much as common sense and plain dealing.",
        "Its amazing how much good you can do if you do not care who gets the credit.",
        "Everyone agrees. You are the best.",
        "Life consist not in holding good cards, but in playing those you hold well.",
        "Jealousy doesn't open doors, it closes them!",
        "It's better to be alone sometimes.",
        "When fear hurts you, conquer it and defeat it!",
        "Let the deeds speak.",
        "You will be called in to fulfill a position of high honor and responsibility.",
        "The man on the top of the mountain did not fall there.",
        "You will conquer obstacles to achieve success.",
        "Joys are often the shadows, cast by sorrows.",
        "Fortune favors the brave.",
    ]
    fortune = random.choice(possible)
    args = {"fortune": fortune}
    page = Page(filename="fortune.html", args=args)
    return page.render()


async def menu(request) -> web.Response:
    """
    This will return
    """
    food_items = [
        {"item": "General Tzo's Chicken", "description": "Yummy chicken on rice", "price": 12.99},
        {"item": "Kung Pao Beef", "description": "Spicy Beef on rice", "price": 13.99}
    ]  # TODO - Update to a sqlite3 database call
    args = {"foods": food_items}
    page = Page(filename="menu.html", args=args)
    return page.render()


async def register(add_to_registry=True):
    print(f"""
    Service Registry {REG_ADDR}:{REG_PORT}

    Adding to the Service Registry:

    service name     {SERVICE}
    service IP       {LOCAL_IP}
    service port     {PORT}
    """)
    if add_to_registry:
        r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/add/{SERVICE}/{LOCAL_IP}/{PORT}")
        print(r.status_code, r.text)


async def unregister(remove_from_registry=True):
    if remove_from_registry:
        r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/remove/{SERVICE}/{LOCAL_IP}/{PORT}")
        print(r.status_code)


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
    app.on_startup.append(register)
    app.on_shutdown.append(unregister)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()