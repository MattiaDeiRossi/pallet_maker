from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from opcua_client import OPCUAReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cambia in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

opc_reader = OPCUAReader(
    url="opc.tcp://localhost:4840",               # server OPC UA
    node_ids=[
        "ns=2;s=Machine/Status",
        "ns=2;s=Machine/Error",
    ],
    username="admin",                              # inserisci utente
    password="password123",                        # inserisci password
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await opc_reader.connect()
    yield
    await opc_reader.disconnect()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await opc_reader.read_all()
            await websocket.send_json(data)
            await asyncio.sleep(1.0)
    except Exception as e:
        print("[WS] Connessione chiusa:", e)
    finally:
        await websocket.close()
