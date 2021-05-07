#!/usr/bin/env python3

"""
An example monolith to practice verifying
the code is able to receive a request on
the /v2/menu path and route it to the menu
microservice.
"""

import json

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
    menu_svc = requests.get("http://127.0.0.1:55555/get_one/menu").text
    print(menu_svc)
    menu_host = json.loads(menu_svc)
    menu_ip = menu_host['endpoints'][0]
    menu_port = menu_host['endpoints'][1]
    r = requests.get(f"http://{menu_ip}:{menu_port}/menu")
    return web.Response(text=r.text, content_type='text/html')


def main():
    app = web.Application()
    routes(app)
    web.run_app(app, host="0.0.0.0", port=3030)


if __name__ == "__main__":
    main()