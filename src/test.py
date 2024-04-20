import json
from pypdf import PdfReader
from annotations import *

pdf_directory = "C://GitLab//aectech-hackathon-2024-tag-it//sample"
src_directory = "C://GitLab//aectech-hackathon-2024-tag-it//src"
json_directory = "C://GitLab//aectech-hackathon-2024-tag-it//json"
reader = PdfReader(pdf_directory + "//A102_Annotated.pdf")

# def extract_line_to_json(line_object):
#     line_json = {}
#     line_json["author"] = line_object["/T"]
#     line_json["subtype"] = line_object["/Subtype"]
#     line_json["bounding_box"] = line_object["/Rect"]
#     line_json["location"] = [[line_object["/L"][0], line_object["/L"][1]], [line_object["/L"][2], line_object["/L"][3]]]
#     line_json["arrow_type"] = [line_object["/LE"][0], line_object["/LE"][1]] if "/LE" in line_object else ['/None', '/None']
#     return line_json

number_of_pages = len(reader.pages)

annotations_export = []

for page in reader.pages:
    if "/Annots" in page:
        # print("Number of annotations on page: ", len(page["/Annots"]))
        for annot in page["/Annots"]:
            obj = annot.get_object()
            subtype = annot.get_object()["/Subtype"]
            print (subtype)
            print (obj)
            x1, y1, x2, y2 = obj["/Rect"]
            location = [[float(x1), float(y1)], [float(x2), float(y2)]]
            if subtype == "/Text":
                annotation = {"subtype": obj["/Subtype"], "content": obj["/Contents"]}
                annotations_export.append(annotation)
            elif subtype == "/Line":
                line_annotation = LineAnnotation(obj)
                annotations_export.append(line_annotation.to_json())
            elif subtype == "/FreeText":
                freetext_annotation = FreeTextAnnotation(obj)
                annotations_export.append(freetext_annotation.to_json())
            elif subtype == "/Highlight":
                    coords = annot.get_object()["/QuadPoints"]
                    x1, y1, x2, y2, x3, y3, x4, y4 = coords
                    annotation = {"subtype": obj["/Subtype"], "content": obj["/Contents"],
                                  # "quad_points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                                  }
                    annotations_export.append(annotation)
            else:
                annotation = {"subtype": obj["/Subtype"], "location": location}
                # print("Annotation type not supported: ", obj["/Subtype"])
            # print(annotation)

# print("Number of annotations to export: ", len(annotations_export))
# Serialize annotations_export
annotations_export_json = json.dumps(annotations_export, indent=4)

save_path = json_directory + "//annotations.json"
# Write to annotations.json file
with open(save_path, 'w') as f:
    f.write(annotations_export_json)

# with open('annotations.json', 'w') as f:
#     f.write(annotations_export_json)