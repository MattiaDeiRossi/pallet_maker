from asyncua import Client, ua
import asyncio


class OPCUAReader:
    def __init__(self, url: str, node_ids: list[str], username: str, password: str):
        self.url = url
        self.node_ids = node_ids
        self.username = username
        self.password = password
        self.client = Client(url)

        # impostazioni di sicurezza
        self.client.set_security_string("Basic256Sha256,SignAndEncrypt,cert.pem,key.pem")

        # login
        self.client.set_user(self.username)
        self.client.set_password(self.password)

        self.nodes = []

    async def connect(self):
        await self.client.connect()
        self.nodes = [self.client.get_node(nid) for nid in self.node_ids]
        print(f"[OPCUA] Connesso a {self.url} come {self.username}")

    async def read_all(self):
        values = await asyncio.gather(*[node.read_value() for node in self.nodes])
        return dict(zip(self.node_ids, values))

    async def disconnect(self):
        await self.client.disconnect()
        print("[OPCUA] Disconnesso")
