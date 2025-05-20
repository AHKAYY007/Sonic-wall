from fastapi import WebSocket
from typing import List

class TrafficManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data):
        for conn in self.connections:
            await conn.send_json(data)

manager = TrafficManager()
