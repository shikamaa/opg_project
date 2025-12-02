from fastapi import FastAPI, HTTPException

app = FastAPI()




@app.get('/')
async def idx():
    return {"msg": "hello"}