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
    if conn:
        return JSONResponse({'hello': (await conn.get('key')).decode('utf-8')})
    else:
        return JSONResponse({'error': 'error connecting to redis'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, lifespan='on')
