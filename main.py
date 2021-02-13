# /usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI

from api.endpoints.v1 import v1_api_router

app = FastAPI()
app.include_router(v1_api_router, prefix='/api/v1')

@app.get('/')
async def root():
    return {'message': 'Hello World.'}
