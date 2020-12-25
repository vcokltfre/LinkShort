from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

from src.database import DatabaseAPI
from src.auth import auth
from config.config import fallback, host_url

app = FastAPI()
db = DatabaseAPI()


class Create(BaseModel):
    url: str
    name: Optional[str]


@app.get("/")
async def index():
    return RedirectResponse(url=fallback, status_code=301)

@app.get("/{urlid}")
async def getlink(urlid: str):
    await db.ensure_init()
    link = await db.get_link(urlid)

    link = link if link else fallback

    return RedirectResponse(url=link, status_code=301)

@app.post("/create")
async def mklink(url: Create, request: Request):
    auth(request)
    await db.ensure_init()

    if url.name and len(url.name) > 32:
        raise HTTPException(400, "Short links must be 32 characters or less.")

    link = await db.create_link(url.url, url.name)
    if not link:
        raise HTTPException(400, "Duplicate short link.")
    return {"status":"success", "data":f"{host_url}/{link}", "code":link}