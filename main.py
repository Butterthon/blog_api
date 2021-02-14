# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from api.endpoints.v1 import v1_api_router
from middlewares import (
    AuthenticationBackend,
    ProcessRequestMiddleware
)

app = FastAPI()

# ミドルウェアの設定
# ・ミドルウェアは 後 に追加したものが先に実行される
# ・CORSMiddlewareは必ず一番 後 に追加すること
# ・ミドルウェアを追加する場合はCORSMiddleware と ProcessRequestMiddlewareより 前 に追加すること
app.add_middleware(
    AuthenticationMiddleware,
    backend=AuthenticationBackend())
app.add_middleware(ProcessRequestMiddleware)

# ルーターの設定
app.include_router(v1_api_router, prefix='/api/v1')

@app.get('/')
async def root():
    return {'message': 'Hello World.'}
