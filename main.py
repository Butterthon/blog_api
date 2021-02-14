# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI

from api.endpoints.v1 import v1_api_router
from middlewares import ProcessRequestMiddleware

app = FastAPI()

# ミドルウェアの設定
app.add_middleware(ProcessRequestMiddleware)

# ルーターの設定
app.include_router(v1_api_router, prefix='/api/v1')

@app.get('/')
async def root():
    return {'message': 'Hello World.'}
