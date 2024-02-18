from fastapi import FastAPI

from api import router

app = FastAPI(
    title='Wildberries web-parser',
    description='API provide methods for parsing wildberries.ru'
)
app.include_router(router=router)


@app.get('/')
def index():
    return {'result': True}
