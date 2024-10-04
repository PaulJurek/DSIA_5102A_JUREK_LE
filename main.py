from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get('/')
async def get_root():
    return {'message':datetime.now().strftime('%d/%m/%Y')}