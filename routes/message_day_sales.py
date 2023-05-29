from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

apiMessageSales = APIRouter()

websocket_list = []


@apiMessageSales.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if websocket not in websocket_list:
        websocket_list.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            for web in websocket_list:
                if web != websocket:
                    await web.send_json(data)
    except WebSocketDisconnect:
        pass
        websocket_list.remove(websocket)
