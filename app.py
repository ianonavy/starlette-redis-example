from starlette.applications import Starlette
from starlette.responses import JSONResponse
import aioredis
import uvicorn

app = Starlette(debug=True)
conn = None

@app.on_event('startup')
async def startup():
    global conn
    conn = await aioredis.create_redis_pool('redis://redis')


@app.route('/')
async def homepage(request):
    try:
        raw_value = await conn.get('key')
        value = raw_value.decode('utf-8')
        response = {'hello': value}
    except:
        response = {'error': 'error while fetching from redis'}
    return JSONResponse(response)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, lifespan='on')
