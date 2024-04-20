import json
from pypdf import PdfReader

pdf_directory = "C://Users//ChenPen//Desktop//AEC Tech 2024"
src_directory = "C://GitLab//aectech-hackathon-2024-tag-it//src"
json_directory = "C://GitLab//aectech-hackathon-2024-tag-it//json"
reader = PdfReader(pdf_directory + "//GENN_APD_112_AIA_ARC_PLA_N1_B_Plan N1.pdf")
# reader = PdfReader(directory + "//20230927 UBC Gateway - Current Architectural_SB- 141.pdf")

number_of_pages = len(reader.pages)

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

save_path = json_directory + "//annotations.json"
# Write to annotations.json file
with open(save_path, 'w') as f:
    f.write(annotations_export_json)

# with open('annotations.json', 'w') as f:
#     f.write(annotations_export_json)