from fastapi import APIRouter, Depends, WebSocket, FastAPI
from app.opcua_client import get_opcua_client, OPCUAClient
import asyncio

router = APIRouter()

@router.get("/info")
async def get_info():
    return {
        "name": "Pallet Maker",
    }

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, opc_client: OPCUAClient = Depends(get_opcua_client)):
    await websocket.accept()
    try:
        while True:
            data = await opc_client.read_all()
            await websocket.send_json(data)
            await asyncio.sleep(1.0)
    except Exception as e:
        print("[WS] Connection closed:", e)
    finally:
        await websocket.close()
