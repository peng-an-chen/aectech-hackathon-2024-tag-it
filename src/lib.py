from pypdf import PdfReader
import json
from watchdog.events import FileSystemEventHandler
from annotations import *

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
        # remove the directory path from the filename and keep only the filename and remove extension
        sheetName = filename.split("/")[-1].split(".")[0]

        # remove (Annotated) from the filename
        if " (Annotated)" in sheetName:
            sheetName = sheetName.replace(" (Annotated)", "")
        
        export = { "sheetName": sheetName }
        with open(filename, "rb") as file:  # Use context manager to handle the file
            reader = PdfReader(file)
            annotations_export = []

            for page in reader.pages:
                pageMediaBox = reader.pages[0].mediabox
                if "/Annots" in page:
                    for annot in page["/Annots"]:
                        obj = annot.get_object()
                        subtype = obj["/Subtype"]
                        print (obj, '\n')
                        if subtype == "/FreeText":
                            freetext_annotation = FreeTextAnnotation(obj)
                            annotations_export.append(freetext_annotation.to_json())
                        elif subtype == "/Line":
                            line_annotation = LineAnnotation(obj)
                            annotations_export.append(line_annotation.to_json())
                        elif subtype == "/PolyLine":
                            polyline_annotation = PolylineAnnotation(obj)
                            annotations_export.append(polyline_annotation.to_json())
                        elif subtype == "/Polygon":
                            polygon_annotation = PolygonAnnotation(obj)
                            annotations_export.append(polygon_annotation.to_json())
                        elif subtype == "/Circle":
                            circle_annotation = CircleAnnotation(obj)
                            annotations_export.append(circle_annotation.to_json())
                        elif subtype == "/Ink":
                            ink_annotation = InkAnnotation(obj)
                            annotations_export.append(ink_annotation.to_json())

                        # if subtype in ["/Text", "/FreeText"]:
                        #     annotation = {
                        #         "subtype": obj["/Subtype"],
                        #         "content": obj.get("/Contents", ""),
                        #         "location": remapped_location
                        #     }
                        #     annotations_export.append(annotation)
                        # elif subtype == "/Highlight":
                        #     coords = obj["/QuadPoints"]
                        #     x1, y1, x2, y2, x3, y3, x4, y4 = coords
                        #     annotation = {
                        #         "subtype": obj["/Subtype"],
                        #         "content": obj.get("/Contents", ""),
                        #         "location": remapped_location
                        #     }
                        #     annotations_export.append(annotation)
                        else:
                            print("Unsupported annotation type:", subtype)

            # Serialize and write annotations to JSON
            export["annotations"] = annotations_export
            export_json = json.dumps(export)
            with open('annotations.json', 'w') as f:
                f.write(export_json)
            print("Processed annotations written to 'annotations.json'.")
