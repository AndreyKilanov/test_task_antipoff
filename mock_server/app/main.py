import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import random
import asyncio

app = FastAPI()

path = Path(__file__).parent.parent / ".env"
load_dotenv(path)

DELAY = os.getenv("DELAY", 60)


@app.post("/result")
async def mock_external_server()-> dict:
    try:
        delay = random.uniform(1, int(DELAY))
        await asyncio.sleep(delay)

        return {"result": random.choice([True, False])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ping")
async def ping() -> dict:
    return {"status": "OK"}
