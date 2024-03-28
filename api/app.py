from fastapi import FastAPI, Depends

from api import router
from services.pragma import PragmaService

app = FastAPI(
    title='Wildberries web-parser',
    description='API provide methods for parsing wildberries.ru'
)
app.include_router(router=router)

@app.get('/')
async def index():
    return {'result': True}


@app.post('/recreate_tables')
async def recreate_tables(service: PragmaService = Depends()):
    await service.recreate_tables()
    return {'result': True}
