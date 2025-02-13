from fastapi import FastAPI, HTTPException
import random
import asyncio

app = FastAPI()

@app.post("/result")
async def mock_external_server()-> dict:
    try:
        delay = random.uniform(1, 60)
        await asyncio.sleep(delay)

        return {"result": random.choice([True, False])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
async def ping() -> dict:
    return {"status": "OK"}
