using Microsoft.Win32;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
//#include <iostream>
//#include <fstream>
//using namespace std;
namespace client
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void ButtonGeneratePlugin_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(deviceInfo.Text))
            {
                Stream myStream;
                UnicodeEncoding uniEncoding = new UnicodeEncoding();
                SaveFileDialog saveFileDialog1 = new SaveFileDialog();
                saveFileDialog1.Filter = "All files (*.*)|*.*";
                saveFileDialog1.Title = "Save an Image File";
                saveFileDialog1.ShowDialog();


                if ((myStream = saveFileDialog1.OpenFile()) != null)
                {
                    // code to write the stream goes here.
                    var sw = new StreamWriter(myStream, uniEncoding);
                    string message = deviceInfo.Text;
                    try
                    {
                        sw.Write(message);
                        sw.Flush();
                    }
                    finally
                    {
                        sw.Dispose();
                    }
                    myStream.Seek(0, SeekOrigin.Begin);   
                    myStream.Close();
 
                }


            }

        }
    }
}