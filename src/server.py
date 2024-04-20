import asyncio
import websockets

class WebSocketServer:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.clients = set()

  async def handle_client(self, websocket, path):
    self.clients.add(websocket)
    try:
      while True:
        message = await websocket.recv()
        print(f"[SERVER] Received message: {message}")
        # Handle incoming messages from clients if needed
    finally:
      self.clients.remove(websocket)

  async def send_message(self, message):
    if self.clients:
      await asyncio.wait([client.send(message) for client in self.clients])

  async def start(self):
    server = await websockets.serve(self.handle_client, self.host, self.port)
    await server.wait_closed()

# Example usage
if __name__ == "__main__":
  server = WebSocketServer("localhost", 8000)
  print("Starting server on port 8000...")
  asyncio.run(server.start())

def createServer():
  server = WebSocketServer("localhost", 8000)
  print("Starting server on port 8000...")
  asyncio.run(server.start())
  return server