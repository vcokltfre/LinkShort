from hmac import compare_digest
from fastapi import Request
from fastapi.exceptions import HTTPException

from config.config import master_token


def auth(request: Request):
    if not "X-Api-Token" in request.headers:
        raise HTTPException(403, "Token required.")
    tok = request.headers["X-Api-Token"]

    if compare_digest(tok, master_token):
        return True

    raise HTTPException(403, "Not authorized.")
