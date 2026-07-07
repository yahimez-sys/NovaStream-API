import asyncio
from fastapi import WebSocket


class WebSocketManager:

    def __init__(self):

        self.connections = set()

        self.loop = None

    # ==========================================
    # Registrar Event Loop
    # ==========================================

    def set_loop(self, loop):

        self.loop = loop

    # ==========================================
    # Cliente conectado
    # ==========================================

    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        self.connections.add(websocket)

    # ==========================================
    # Cliente desconectado
    # ==========================================

    def disconnect(self, websocket: WebSocket):

        self.connections.discard(websocket)

    # ==========================================
    # Enviar mensaje a todos
    # ==========================================

    async def broadcast(self, message):

        dead = []

        for ws in list(self.connections):

            try:

                await ws.send_json(message)

            except:

                dead.append(ws)

        for ws in dead:

            self.disconnect(ws)

    # ==========================================
    # Broadcast desde código síncrono
    # ==========================================

    def send(self, message):

        if self.loop is None:

            return

        asyncio.run_coroutine_threadsafe(

            self.broadcast(message),

            self.loop

        )


ws_manager = WebSocketManager()