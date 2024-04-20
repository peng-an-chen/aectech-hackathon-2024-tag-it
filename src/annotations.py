__all__ = ["FreeTextAnnotation", "LineAnnotation"]

class BaseAnnotation(object):
    def __init__(self, pypdf_obj):
        self.date = pypdf_obj['/CreationDate']
        self.subtype = pypdf_obj['/Subtype']
        self.author = pypdf_obj['/T']
        self.bounding_box = [[pypdf_obj['/Rect'][0], pypdf_obj['/Rect'][1]],
                             [pypdf_obj['/Rect'][2], pypdf_obj['/Rect'][3]]]

    def to_json(self):
        return {
            "author": self.author,
            "subtype": self.subtype,
            "bounding_box": self.bounding_box,
            "date": self.date
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