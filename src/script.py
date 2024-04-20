import time
from watchdog.observers import Observer
from lib import PDFChangeHandler

# Main setup for watchdog
directory_to_watch = "./sample/"  # Watching the current directory
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
