from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title='Wildberries web-parser',
    description='API provide methods for parsing wildberries.ru'
)


@app.get('/')
def index():
    return {'result': True}