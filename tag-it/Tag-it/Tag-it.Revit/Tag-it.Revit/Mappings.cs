using Autodesk.Revit.DB;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tag_it.Revit
{
    public class Mappings
    {
        public string AnnotationJson = string.Empty;
        public List<ViewSheet> RevitSheets = new List<ViewSheet>();
        public List<string> SheetNames = new List<string>();
        public string SelectedSheetName;
        public string SheetName;

        public Mappings()
        {
            SelectedSheetName = SheetNames.FirstOrDefault();
        }
    }
}
