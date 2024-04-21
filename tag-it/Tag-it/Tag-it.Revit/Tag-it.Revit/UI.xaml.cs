using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;
using System.Collections.ObjectModel;
using System.ComponentModel;
using PropertyChanged;

namespace Tag_it.Revit
{
    /// <summary>
    /// Interaction logic for UI.xaml
    /// </summary>
    [AddINotifyPropertyChangedInterface]
    public partial class Ui : Window, INotifyPropertyChanged
    {
        /// <summary>
        /// The event that fires when any child property changes its value
        /// </summary>
        public event PropertyChangedEventHandler PropertyChanged = (sender, e) => { };

        private readonly Document _doc;

        //private readonly UIApplication _uiApp;
        //private readonly Autodesk.Revit.ApplicationServices.Application _app;
        private readonly UIDocument _uiDoc;

        private readonly EventHandlerWithStringArg _mExternalMethodStringArg;
        private readonly EventHandlerWithWpfArg _mExternalMethodWpfArg;

        public string MarkupFolder = string.Empty;
        public ObservableCollection<Mappings> SheetMappings = new ObservableCollection<Mappings>() { new Mappings("sheet1", new List<string>() { "sheet", "anothersheet" }), new Mappings("sheet1", new List<string>() { "sheet", "anothersheet" }) };

        public string NameSheet = "A102 Plans";
        public static List<string> Names = new List<string>() { "A001 Title Sheet", "A101 Site Plan", "A102 Plans", "A103 Elevations/Sections", "A104 Elev./Sec./Det.", "A105 Elev./ Stair Sections" };
        public string SelectedName = Names.FirstOrDefault();

        public Ui(UIApplication uiApp, EventHandlerWithStringArg evExternalMethodStringArg,
            EventHandlerWithWpfArg eExternalMethodWpfArg)
        {
            _uiDoc = uiApp.ActiveUIDocument;
            _doc = _uiDoc.Document;
            //_app = _doc.Application;
            //_uiApp = _doc.Application;
            Closed += MainWindow_Closed;

            Mappings newMapping = new Mappings();
            
            string sheetName = "Sheet 1";

            if (!string.IsNullOrEmpty(sheetName))
            {
                newMapping.SheetName = sheetName;
                for (int i = 0; i < 3; i++)
                {
                    newMapping.SheetNames.Add("Sheet A" + (i+1).ToString());
                }

                newMapping.SelectedSheetName = newMapping.SheetNames.FirstOrDefault();
                SheetMappings.Add(newMapping);
            }
            RaisePropertyChanged("SheetMappings");

            InitializeComponent();
            _mExternalMethodStringArg = evExternalMethodStringArg;
            _mExternalMethodWpfArg = eExternalMethodWpfArg;
        }


        private void MainWindow_Closed(object sender, EventArgs e)
        {
            Close();
        }

        #region External Project Methods

        private void BExtString_Click(object sender, RoutedEventArgs e)
        {
            // Raise external event with a string argument. The string MAY
            // be pulled from a Revit API context because this is an external event
            _mExternalMethodStringArg.Raise($"Title: {_doc.Title}");
        }

        private void SelectFolderCommand_Click(object sender, RoutedEventArgs e)
        {
            Methods.SelectFolder(this, _doc);
            Methods.LoadAnnotations(this, _doc);
            UserAlert();
        }

        private void MapMarkupCommand_Click(object sender, RoutedEventArgs e)
        {
        }

        #endregion

        #region Non-External Project Methods

        private void UserAlert()
        {
            //TaskDialog.Show("Non-External Method", "Non-External Method Executed Successfully");
            MessageBox.Show("Non-External Method Executed Successfully", "Non-External Method");

            //Dispatcher.Invoke(() =>
            //{
            //    TaskDialog mainDialog = new TaskDialog("Non-External Method")
            //    {
            //        MainInstruction = "Hello, Revit!",
            //        MainContent = "Non-External Method Executed Successfully",
            //        CommonButtons = TaskDialogCommonButtons.Ok,
            //        FooterText = "<a href=\"http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=2484975 \">"
            //                     + "Click here for the Revit API Developer Center</a>"
            //    };


            //    TaskDialogResult tResult = mainDialog.Show();
            //    Debug.WriteLine(tResult.ToString());
            //});
        }

        private void BNonExternal3_Click(object sender, RoutedEventArgs e)
        {
            // the sheet takeoff + delete method won't work here because it's not in a valid Revit api context
            // and we need to do a transaction
            // Methods.SheetRename(this, _doc); <- WON'T WORK HERE
            UserAlert();
        }

        private void BNonExternal1_Click(object sender, RoutedEventArgs e)
        {
            Methods.DocumentInfo(this, _doc);
            UserAlert();
        }

        private void BNonExternal2_Click(object sender, RoutedEventArgs e)
        {
            Methods.WallInfo(this, _doc);
            UserAlert();
        }

        #endregion
        public void RaisePropertyChanged(string propertyName)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
}
