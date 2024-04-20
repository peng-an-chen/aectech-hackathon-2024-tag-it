import json
from PyPDF2 import PdfReader

file_one = "GENN_APD_112_AIA_ARC_PLA_N1_B_Plan N1.pdf"
file_two = "20230927 UBC Gateway - Current Architectural_SB- 141.pdf"

reader = PdfReader(file_two)

print("File name: ", file_two)

annotations_export = []

for page in reader.pages:
    if "/Annots" in page:
        print("Number of annotations on page: ", len(page["/Annots"]))
        for annot in page["/Annots"]:
            subtype = annot.get_object()["/Subtype"]
            obj = annot.get_object()
            x1, y1, x2, y2 = obj["/Rect"]
            print(float(x1))
            location = [[float(x1), float(y1)], [float(x2), float(y2)]]
            if subtype == "/Text":
                annotation = {"subtype": obj["/Subtype"], "content": obj["/Contents"]}
                annotations_export.append(annotation)

            elif subtype == "/FreeText":
                annotation = {"subtype": obj["/Subtype"], "content": obj["/Contents"], "location": location}
                annotations_export.append(annotation)

            elif subtype == "/Highlight":
                    coords = annot.get_object()["/QuadPoints"]
                    x1, y1, x2, y2, x3, y3, x4, y4 = coords
                    annotation = {"subtype": obj["/Subtype"], "content": obj["/Contents"],
                                  # "quad_points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                                  }
                    annotations_export.append(annotation)
            else:
                # annotation = {"subtype": obj["/Subtype"], "location": location}
                print("Annotation type not supported: ", obj["/Subtype"])
            print(annotation)

print("Number of annotations to export: ", len(annotations_export))
# Serialize annotations_export
annotations_export_json = json.dumps(annotations_export)

# Write to annotations.json file
with open('annotations.json', 'w') as f:
    f.write(annotations_export_json)