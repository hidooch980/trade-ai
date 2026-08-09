from fastapi.encoders import jsonable_encoder
import json
from fastapi import WebSocket
import json
from datetime import datetime, date


class SocketManager:

    def __init__(self):
        self.active_connections = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)


    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)


    def json_safe(self, obj):

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        if isinstance(obj, dict):
            return {k: self.json_safe(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self.json_safe(i) for i in obj]

        return obj


    async def broadcast(self, data):

        safe_data = self.json_safe(data)

        for connection in self.active_connections:
            try:
                await connection.send_json(safe_data)
            except Exception:
                self.disconnect(connection)


socket_manager = SocketManager()
