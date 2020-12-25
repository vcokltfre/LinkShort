from aiomysql import create_pool
from asyncio import get_event_loop
from pathlib import Path

from config.config import creds
from .tools import IDGenerator

cmds = {}

def get_command(name: str):
    if name in cmds:
        return cmds[name]
    p = Path(f"./src/data/{name}.sql")
    if not p.exists():
        raise FileNotFoundError(f"Command file {p} doesn't exist!")
    with p.open() as f:
        data = f.read()
        cmds[name] = data
        return data


class DatabaseAPI:
    def __init__(self):
        self.has_init = False
        self.idg = IDGenerator()

    async def ensure_init(self):
        if not self.has_init:
            self.has_init = True
            await self.init()

    async def init(self):
        self.pool = await create_pool(**creds, loop=get_event_loop())

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(get_command("init"))

    async def create_link(self, url: str, name: str = None) -> str:
        link = self.idg.next() if not name else name
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("INSERT INTO Urls (link_name, link) VALUES (%s, %s);", (link, url))
                await conn.commit()
            return link
        except:
            return False

    async def get_link(self, link: str) -> str:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM Urls WHERE link_name = %s;", link)
                url = await cur.fetchone()
                if not url:
                    return None
                url = url[1:]
                await cur.execute("UPDATE Urls SET clicks = %s WHERE link_name = %s;", (url[1] + 1, link))
            await conn.commit()
        return url[0]