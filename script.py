import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader

class PDFChangeHandler(FileSystemEventHandler):
    def __init__(self, filename):
        self.filename = filename

    def on_any_event(self, event):
        if event.is_directory:
            return  # Ignore directory events
        if event.event_type in ['modified', 'moved', 'created'] and event.src_path.endswith(self.filename):
            print(f"{self.filename} event detected: {event.event_type}. Processing annotations...")
            self.process_pdf(event.src_path)

    def process_pdf(self, filename):
        with open(filename, "rb") as file:  # Use context manager to handle the file
            reader = PdfReader(file)
            annotations_export = []

            for page in reader.pages:
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        obj = annot.get_object()
                        subtype = obj["/Subtype"]
                        x1, y1, x2, y2 = obj["/Rect"]
                        location = [[float(x1), float(y1)], [float(x2), float(y2)]]

                        if subtype in ["/Text", "/FreeText"]:
                            annotation = {
                                "subtype": obj["/Subtype"],
                                "content": obj.get("/Contents", ""),
                                "location": location if subtype == "/FreeText" else None
                            }
                            annotations_export.append(annotation)
                        elif subtype == "/Highlight":
                            coords = obj["/QuadPoints"]
                            x1, y1, x2, y2, x3, y3, x4, y4 = coords
                            annotation = {
                                "subtype": obj["/Subtype"],
                                "content": obj.get("/Contents", ""),
                                # "quad_points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                            }
                            annotations_export.append(annotation)
                        else:
                            print("Unsupported annotation type:", subtype)

            # Serialize and write annotations to JSON
            annotations_export_json = json.dumps(annotations_export)
            with open('annotations.json', 'w') as f:
                f.write(annotations_export_json)
            print("Processed annotations written to 'annotations.json'.")

# Main setup for watchdog
directory_to_watch = "./sample/"  # Watching the current directory
file_to_watch = "sample/A102_Annotated.pdf"
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
