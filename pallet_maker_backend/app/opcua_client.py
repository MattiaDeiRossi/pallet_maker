from asyncua import Client
import asyncio
from app.config import *
import logging

logging.basicConfig(level=logging.INFO)

class OPCUAClient:
    def __init__(self, url: str, node_ids: list[str], username: str, password: str):
        self.url = url
        self.node_ids = node_ids
        self.username = username
        self.password = password
        self.client = Client(url)

        self.client.set_user(self.username)
        self.client.set_password(self.password)
        self.nodes = []
        self.logger = logging.getLogger("asyncua")

    async def connect(self):
        await self.client.connect()
        await self.client.set_security_string("Basic256Sha256,SignAndEncrypt,cert.pem,key.pem")
        self.nodes = [self.client.get_node(nid) for nid in self.node_ids]
        self.logger.info(f"[OPCUA] Connected to {self.url}")

    async def read_all(self):
        values = await asyncio.gather(*[node.read_value() for node in self.nodes])
        return dict(zip(self.node_ids, values))

    async def disconnect(self):
        await self.client.disconnect()
        self.logger.info("[OPCUA] Disconnected")

opc_client = OPCUAClient(
    url=URL,               
    node_ids=NODE_IDS,
    username=USERNAME,                              
    password=PASSWORD,                        
)

async def get_opcua_client() -> OPCUAClient:
    return opc_client
