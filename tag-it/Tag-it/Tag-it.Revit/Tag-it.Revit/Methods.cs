using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Autodesk.Revit.DB;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Tag_it.Revit
{
    /// <summary>
    /// Create methods here that need to be wrapped in a valid Revit Api context.
    /// Things like transactions modifying Revit Elements, etc.
    /// </summary>
    internal class Methods
    {
        /// <summary>
        /// Method for collecting sheets as an asynchronous operation on another thread.
        /// </summary>
        /// <param name="doc">The Revit Document to collect sheets from.</param>
        /// <returns>A list of collected sheets, once the Task is resolved.</returns>
        private static async Task<List<ViewSheet>> GetSheets(Document doc)
        {
            return await Task.Run(() =>
            {
                Util.LogThreadInfo("Get Sheets Method");
                return new FilteredElementCollector(doc)
                    .OfClass(typeof(ViewSheet))
                    .Select(p => (ViewSheet)p).ToList();
            });
        }

        /// <summary>
        /// Rename all the sheets in the project. This opens a transaction, and it MUST be executed
        /// in a "Valid Revit API Context", otherwise the add-in will crash. Because of this, we must
        /// wrap it in a ExternalEventHandler, as we do in the App.cs file in this template.
        /// </summary>
        /// <param name="ui">An instance of our UI class, which in this template is the main WPF
        /// window of the application.</param>
        /// <param name="doc">The Revit Document to rename sheets in.</param>
        public static void SheetRename(Ui ui, Document doc)
        {
            Util.LogThreadInfo("Sheet Rename Method");

            // get sheets - note that this may be replaced with the Async Task method above,
            // however that will only work if we want to only PULL data from the sheets,
            // and executing a transaction like below from an async collection, will crash the app
            List<ViewSheet> sheets = new FilteredElementCollector(doc)
                .OfClass(typeof(ViewSheet))
                .Select(p => (ViewSheet)p).ToList();

            // report results - push the task off to another thread
            Task.Run(() =>
            {
                Util.LogThreadInfo("Sheet Rename Show Results");

                // report the count
                string message = $"There are {sheets.Count} Sheets in the project";
                ui.Dispatcher.Invoke(() =>
                    ui.TbDebug.Text += "\n" + (DateTime.Now).ToLongTimeString() + "\t" + message);
            });

            // rename all the sheets, but first open a transaction
            using (Transaction t = new Transaction(doc, "Rename Sheets"))
            {
                Util.LogThreadInfo("Sheet Rename Transaction");

                // start a transaction within the valid Revit API context
                t.Start("Rename Sheets");

                // loop over the collection of sheets using LINQ syntax
                foreach (string renameMessage in from sheet in sheets
                                                 let renamed = sheet.LookupParameter("Sheet Name")?.Set("TEST")
                                                 select $"Renamed: {sheet.Title}, Status: {renamed}")
                {
                    ui.Dispatcher.Invoke(() =>
                        ui.TbDebug.Text += "\n" + (DateTime.Now).ToLongTimeString() + "\t" + renameMessage);
                }

                t.Commit();
                t.Dispose();
            }

            // invoke the UI dispatcher to print the results to report completion
            ui.Dispatcher.Invoke(() =>
                ui.TbDebug.Text += "\n" + (DateTime.Now).ToLongTimeString() + "\t" + "SHEETS HAVE BEEN RENAMED");
        }

        /// <summary>
        /// Print the Title of the Revit Document on the main text box of the WPF window of this application.
        /// </summary>
        /// <param name="ui">An instance of our UI class, which in this template is the main WPF
        /// window of the application.</param>
        /// <param name="doc">The Revit Document to print the Title of.</param>
        public static void DocumentInfo(Ui ui, Document doc)
        {
            ui.Dispatcher.Invoke(() => ui.TbDebug.Text += "\n" + (DateTime.Now).ToLongTimeString() + "\t" + doc.Title);
        }

        /// <summary>
        /// Count the walls in the Revit Document, and print the count
        /// on the main text box of the WPF window of this application.
        /// </summary>
        /// <param name="ui">An instance of our UI class, which in this template is the main WPF
        /// window of the application.</param>
        /// <param name="doc">The Revit Document to count the walls of.</param>
        public static void WallInfo(Ui ui, Document doc)
        {
            Task.Run(() =>
            {
                Util.LogThreadInfo("Wall Count Method");

                // get all walls in the document
                ICollection<Wall> walls = new FilteredElementCollector(doc)
                    .OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
                    .Select(p => (Wall)p).ToList();

                // format the message to show the number of walls in the project
                string message = $"There are {walls.Count} Walls in the project";

                // invoke the UI dispatcher to print the results to the UI
                ui.Dispatcher.Invoke(() =>
                    ui.TbDebug.Text += "\n" + (DateTime.Now).ToLongTimeString() + "\t" + message);
            });
        }
        /// <summary>
        /// Check the specified folder and load the annotations. 
        /// </summary>
        /// <param name="ui">An instance of our UI class, which in this template is the main WPF
        /// window of the application.</param>
        /// <param name="doc">The current Revit Document</param>
        [STAThread]
        public static void LoadAnnotations(Ui ui, Document doc)
        {
            if (doc.IsValidObject)
            {
                Task.Run(() =>
                {
                    Util.LogThreadInfo("Load Annotations from folder");

                    if (Directory.Exists(ui.MarkupFolder))
                    {
                        string[] files = Directory.GetFiles(ui.MarkupFolder);

                        for (int i = 0; i < files.Length; i++)
                        {
                            string file = files[i];
                            if (file.Contains("annotations") && file.EndsWith(".json"))
                            {
                                Mappings newMapping = new Mappings();
                                newMapping.AnnotationJson = file;
                                string sheetName = "";
                                ReadAnnotationsFile(file, ref sheetName);
                                if (!string.IsNullOrEmpty(sheetName))
                                {
                                    newMapping.SheetName = sheetName;
                                    List<ViewSheet> sheets = GetSheets(doc).Result;
                                    newMapping.RevitSheets = sheets;
                                    foreach (var sheet in sheets)
                                    {
                                        newMapping.SheetNames.Add(sheet.Title);
                                    }                                    
                                    newMapping.SelectedSheetName = newMapping.SheetNames.FirstOrDefault();
                                    ui.SheetMappings.Add(newMapping);
                                }
                            }
                        }
                        
                    }

                });
            }
        }
        /// <summary>
        /// Select the folder that contains the annotated PDF Mark-ups.
        /// </summary>
        /// <param name="ui">An instance of our UI class, which in this template is the main WPF
        /// window of the application.</param>
        /// <param name="doc">The current Revit Document</param>
        public static void SelectFolder(Ui ui, Document doc)
        {
            if (doc.IsValidObject)
            {
                Util.LogThreadInfo("Load Markup Folder");

                FolderBrowserDialog folder = new FolderBrowserDialog();
                // Set the help text description for the FolderBrowserDialog.
                folder.Description = "Select the directory that contains the PDF Mark-ups to use";

                // Do not allow the user to create new files via the FolderBrowserDialog.
                folder.ShowNewFolderButton = false;

                // Default to the My Documents folder.
                folder.RootFolder = Environment.SpecialFolder.Desktop;

                // Show the FolderBrowserDialog.
                DialogResult result = folder.ShowDialog();
                if (result == DialogResult.OK)
                {
                    ui.MarkupFolder = folder.SelectedPath;
                }
            }
        }
        private static void ReadAnnotationsFile(string file, ref string sheetName)
        {
            // read JSON directly from a file
            using (StreamReader jsonFile = File.OpenText(file))
            using (JsonTextReader reader = new JsonTextReader(jsonFile))
            {
                JObject o2 = (JObject)JToken.ReadFrom(reader);

                if(o2.ContainsKey("sheetName"))
                {
                    sheetName = o2.GetValue("sheetName").ToString();
                }
         
            }
        }
    }
}
