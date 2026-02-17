"""WebSocket server for Cube operations."""
import json
import asyncio


class CubeWSServer:
    """Async WebSocket handler for cube ops."""

    def __init__(self, system):
        self.system = system

    async def handle(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            resp = await self.dispatch(action, data)
            await websocket.send(json.dumps(resp))

    async def dispatch(self, action, data):
        if action == "initialize":
            cid = data.get("cube_id", "default")
            self.system.create_cube(cid)
            return {"status": "initialized", "cube": cid}

        if action == "process":
            cid = data.get("cube_id", "default")
            cube = self.system.cubes.get(cid)
            if not cube:
                return {"error": "cube not found"}
            v = data.get("vertex", "NEU")
            result = await cube.process_vertex(v, data.get("text", ""))
            return {"vertex": v, "result": result}

        if action == "status":
            return {"cubes": {k: c.status() for k, c in self.system.cubes.items()}}

        return {"error": "unknown action"}
