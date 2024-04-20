__all__ = ["FreeTextAnnotation", "LineAnnotation", "PolylineAnnotation", "PolygonAnnotation", "CircleAnnotation", "InkAnnotation"]

class BaseAnnotation(object):
    def __init__(self, pypdf_obj):
        self.date = pypdf_obj['/CreationDate']
        self.subtype = pypdf_obj['/Subtype']
        self.author = pypdf_obj['/T']
        self.color = pypdf_obj['/C']
        self.bounding_box = [[pypdf_obj['/Rect'][i], pypdf_obj['/Rect'][i + 1]] for i in range(0, len(pypdf_obj['/Rect']), 2)]
        self.contents = pypdf_obj['/Contents'] if '/Contents' in pypdf_obj else None

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
        self.location = [[pypdf_obj["/L"][0], pypdf_obj["/L"][1]], [pypdf_obj["/L"][2], pypdf_obj["/L"][3]]]
        self.arrow_type = [pypdf_obj["/LE"][0], pypdf_obj["/LE"][1]] if "/LE" in pypdf_obj else ['/None', '/None']

    def to_json(self):
        json_dict = super().to_json()
        json_dict["location"] = self.location
        json_dict["arrow_type"] = self.arrow_type
        return json_dict
    

class PolylineAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.vertices = pypdf_obj['/Vertices']
        self.interior_color = pypdf_obj['/IC']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["vertices"] = [[self.vertices[i], self.vertices[i + 1]] for i in range(0, len(self.vertices), 2)]
        json_dict["interior_color"] = self.interior_color
        return json_dict
    

class PolygonAnnotation(BaseAnnotation):
    def __init__(self, pypdf_obj):
        super().__init__(pypdf_obj)
        self.vertices = pypdf_obj['/Vertices']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["vertices"] = [[self.vertices[i], self.vertices[i + 1]] for i in range(0, len(self.vertices), 2)]
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
        self.ink_list = pypdf_obj['/InkList'][0]
        self.border_width = pypdf_obj['/BS']['/W']
        self.border_style = pypdf_obj['/BS']['/S']
        self.border_type = pypdf_obj['/BS']['/Type']
    
    def to_json(self):
        json_dict = super().to_json()
        json_dict["subject"] = self.subject
        json_dict["border_width"] = self.border_width
        json_dict["border_style"] = self.border_style
        json_dict["border_type"] = self.border_type
        json_dict["ink_list"] = [[self.ink_list[i], self.ink_list[i + 1]] for i in range(0, len(self.ink_list), 2)]
        return json_dict
