from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.opcua_client import get_opcua_client
from contextlib import asynccontextmanager
import logging

logging.getLogger("asyncua")

@asynccontextmanager
async def lifespan(app: FastAPI):
    opc_client = await get_opcua_client()
    try:
        await opc_client.connect()
    except Exception as e:
        opc_client.logger.error(f"Failed to connect OPC UA client: {e}")
    yield 
    await opc_client.disconnect()

app = FastAPI(title="Pallet Maker", version="1.0.0",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/api")