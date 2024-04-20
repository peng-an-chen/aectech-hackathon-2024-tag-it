__all__ = ["FreeTextAnnotation", "LineAnnotation", "PolylineAnnotation", "PolygonAnnotation", "CircleAnnotation", "InkAnnotation"]



class BaseAnnotation(object):
    def __init__(self, pypdf_obj):
        self.date = pypdf_obj['/CreationDate']
        self.subtype = pypdf_obj['/Subtype']
        self.author = pypdf_obj['/T']
        self.color = pypdf_obj['/C']
        self.contents = pypdf_obj['/Contents'] if '/Contents' in pypdf_obj else None
        self.page = pypdf_obj['/P']
        self.page_media_box = self.page["/MediaBox"]
        self.bounding_box = self.getRemappedBBox(pypdf_obj)

    def getRemappedBBox(self, pypdf_obj):
        x1, y1, x2, y2 = pypdf_obj["/Rect"]
        x1 = x1 / self.page_media_box[2]
        x2 = x2 / self.page_media_box[2]
        y1 = y1 / self.page_media_box[3]
        y2 = y2 / self.page_media_box[3]
        return [[x1, y1], [x2, y2]]
    
    def getRemappedVertices(self, list_of_points):
        remapped_points = []
        for i in range(0, len(list_of_points), 2):
            x = list_of_points[i] / self.page_media_box[2]
            y = list_of_points[i + 1] / self.page_media_box[3]
            remapped_points.append([x, y])
        return remapped_points

    def to_json(self):
        return {
            "date": self.date,
            "subtype": self.subtype,
            "author": self.author,
            "color": self.color,
            "bounding_box": self.bounding_box,
            "contents": self.contents
        }


class FreeTextAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.contents = pypdf_obj['/Contents']

    def to_json(self):
        json_dict = super().to_json()
        json_dict["contents"] = self.contents
        return json_dict
    

class LineAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.location = self.getRemappedVertices(pypdf_obj["/L"])
        self.arrow_type = [pypdf_obj["/LE"][0], pypdf_obj["/LE"][1]] if "/LE" in pypdf_obj else ['/None', '/None']

    def to_json(self):
        json_dict = super().to_json()
        json_dict["location"] = self.location
        json_dict["arrow_type"] = self.arrow_type
        return json_dict
    

class PolylineAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.vertices = self.getRemappedVertices(pypdf_obj['/Vertices'])
        self.interior_color = pypdf_obj['/IC']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["vertices"] = self.vertices
        json_dict["interior_color"] = self.interior_color
        return json_dict
    

class PolygonAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.vertices = self.getRemappedVertices(pypdf_obj['/Vertices'])
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["vertices"] = self.vertices
        return json_dict


class CircleAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.subject = pypdf_obj['/Subj']
        self.radius = pypdf_obj['/RD']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["subject"] = self.subject
        json_dict["radius"] = self.radius
        return json_dict


class InkAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.subject = pypdf_obj['/Subj']
        self.ink_list = self.getRemappedVertices(pypdf_obj['/InkList'][0])
        self.border_width = pypdf_obj['/BS']['/W']
        self.border_style = pypdf_obj['/BS']['/S']
        self.border_type = pypdf_obj['/BS']['/Type']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["subject"] = self.subject
        json_dict["border_width"] = self.border_width
        json_dict["border_style"] = self.border_style
        json_dict["border_type"] = self.border_type
        json_dict["ink_list"] = self.ink_list
        return json_dict
