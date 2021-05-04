#!/usr/bin/env python3

"""
An example monolith to practice verifying
the code is able to receive a request on
the /menu path and route it through to
"http://v2.dragon-cafe.com/menu"
"""

from aiohttp import web
import requests


def routes(app):
    app.add_routes(
            [
                web.get("/v2/menu", menu_v2)
            ]
        )


async def menu_v2(request) -> web.Response:
    print(request)
    r = requests.get("http://v2.dragon-cafe.com/menu")
    return web.Response(text=r.text, content_type='text/html')


def main():
    app = web.Application()
    routes(app)
    web.run_app(app, host="0.0.0.0", port=3030)


if __name__ == "__main__":
    main()