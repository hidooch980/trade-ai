from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.websocket.socket_manager import socket_manager

router = APIRouter()


@router.websocket("/ws/market")
async def market_socket(websocket: WebSocket):

    await socket_manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
