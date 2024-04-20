import time
from watchdog.observers import Observer
from lib import PDFChangeHandler
# from server import createServer
from multiprocessing import Process

# Function to setup and run the WebSocket server
# def run_server():
#     server = createServer()
#     server.run_forever()

# Function to setup and run the file observer
def run_observer():
    directory_to_watch = "./sample/"
    file_to_watch = "sample/A102 Plans (Annotated).pdf"
    event_handler = PDFChangeHandler(file_to_watch)

    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)
    observer.start()

    try:
        print(f"Watching for changes in {directory_to_watch}. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()



if __name__ == '__main__':
      # Create and start separate processes for the server and the observer
#   server_process = Process(target=run_server)
  observer_process = Process(target=run_observer)

#   server_process.start()
  observer_process.start()

  # Wait for both processes to finish
#   server_process.join()
#   observer_process.join()