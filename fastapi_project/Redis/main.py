from fastapi import FastAPI
from redis import Redis
import httpx
import json

app=FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.redis=Redis(host='localhost',port=6379)
    app.state.http_client=httpx.AsyncClient()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()


@app.get('/trending')
async def read_item():
    cached=app.state.redis.get('entries')

    if cached:
        return json.loads(cached)

    if cached is None:
        response=await app.state.http_client.get('https://jsonplaceholder.typicode.com/comments')
        cached=response.json()
        data_str=json.dumps(cached)
        app.state.redis.set("entries",data_str,ex=60)


    return data_str





