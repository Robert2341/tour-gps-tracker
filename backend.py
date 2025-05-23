# backend.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio, random

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

riders = {
    "Pogacar": {"lat": 48.8566, "lng": 2.3522},
    "Vingegaard": {"lat": 48.8567, "lng": 2.3523},
    "Evenepoel": {"lat": 48.8568, "lng": 2.3521},
    "Pidcock": {"lat": 48.8565, "lng": 2.3524},
}

def update_location(loc):
    loc["lat"] += random.uniform(-0.0005, 0.0005)
    loc["lng"] += random.uniform(-0.0005, 0.0005)
    return loc

@app.websocket("/ws/gps")
async def gps_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        for rider in riders:
            riders[rider] = update_location(riders[rider])
        await websocket.send_json(riders)
        await asyncio.sleep(1)

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
