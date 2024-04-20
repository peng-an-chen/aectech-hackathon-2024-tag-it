import asyncio
import websockets

# Store all connected clients
connected_clients = set()

async def echo(websocket, path):
  # Add the new client to the set of connected clients
  connected_clients.add(websocket)
  print("Connected")

  try:
    async for message in websocket:
      print(f"Received message: {message}")
      # Send the message to all connected clients except the sender
      for client in connected_clients:
        if client != websocket:
          await client.send(message)
  except websockets.exceptions.ConnectionClosedOK:
    print("Connection closed")
  finally:
    # Remove the client from the set of connected clients
    connected_clients.remove(websocket)

async def main():
  async with websockets.serve(echo, "localhost", 8000):
    print("Server started")
    await asyncio.Future()  # run forever

asyncio.run(main())