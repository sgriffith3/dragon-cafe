#!/usr/bin/env python3

from aiohttp import web
import os
import aiosqlite
import datetime
import random
import subprocess
import jinja2
import pwd
import grp

PORT = os.getenv("SR_PORT", 55555)
HOST = os.getenv("SR_HOST", "0.0.0.0")
DB_NAME = os.getenv("SR_DB_NAME", "service_registry.db")


def routes(app: web.Application) -> None:
    app.add_routes(
        [
            web.get("/add/{service}/{ip}/{port}", add_service),
            web.get("/remove/{service}/{ip}/{port}", remove_service),
            web.get("/heartbeat/{service}/{ip}/{port}", heartbeat),
            web.get("/get/{service}", get_service),
            web.get("/get_one/{service}", get_one_service)
        ]
    )
    return None


async def add_service(request):
    service = request.match_info.get('service')
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    print(f"Adding the {service} service")
    async with aiosqlite.connect(DB_NAME) as db:
        sql = f"CREATE TABLE IF NOT EXISTS {service} (ip CHAR(16), port INT, heartbeat CHAR(50), alive  BOOL);"
        await db.execute(sql)
        await db.commit()
        now = datetime.datetime.now()
        sql2 = f"INSERT INTO {service} (ip, port, heartbeat, alive) VALUES ('{ip}', '{port}', '{now}', 'TRUE');"
        try:
            await db.execute(sql2)
            await db.commit()
            txt = ""
        except aiosqlite.IntegrityError as err:
            txt = f"{service} service already exists"
    return web.Response(text=txt)


async def heartbeat(request):
    service = request.match_info.get('service')
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    print(f"Adding heartbeat")
    async with aiosqlite.connect(DB_NAME) as db:
        now = datetime.datetime.now()
        sql = f"UPDATE {service} set heartbeat = '{now}' where ip like '{ip}' AND port like '{port}';"
        await db.execute(sql)
        await db.commit()
    return web.Response()


async def remove_service(request):
    service = request.match_info.get('service')
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    print(f"Removing {ip} from the {service} service")
    async with aiosqlite.connect(DB_NAME) as db:
        now = datetime.datetime.now()
        sql = f"UPDATE {service} set heartbeat = '{now}', alive = 'FALSE' where ip like '{ip}' AND port like '{port}';"
        print(sql)
        await db.execute(sql)
        await db.commit()
    return web.Response()


async def get_service(request):
    service = request.match_info.get('service')
    async with aiosqlite.connect(DB_NAME) as db:
        sql = f"SELECT DISTINCT ip,port from {service} where alive = 'TRUE';"
        resp = await db.execute(sql)
        await db.commit()
        fetched = await resp.fetchall()
        services = {'endpoints': fetched}
    return web.json_response(services)


async def get_one_service(request):
    service = request.match_info.get('service')
    async with aiosqlite.connect(DB_NAME) as db:
        sql = f"SELECT ip,port from {service} where alive = 'TRUE';"
        resp = await db.execute(sql)
        await db.commit()
        fetched = await resp.fetchall()
    chosen = random.choice(fetched)
    services = {'endpoints': chosen}
    return web.json_response(services)


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
