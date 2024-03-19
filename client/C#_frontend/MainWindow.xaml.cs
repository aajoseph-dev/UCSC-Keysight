using System;
using System.Diagnostics;
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

namespace client
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void ButtonGeneratePlugin_Click(object sender, RoutedEventArgs e)
        {
            if (deviceInfo != null && category != null &&
                !string.IsNullOrWhiteSpace(deviceInfo.Text) && !string.IsNullOrWhiteSpace(category.Text))
            {
                MessageBox.Show($@"C:\Users\xuedo\OneDrive\Desktop\UCSC-Keysight\api\orchestra.py {deviceInfo.Text} {category.Text}");

                Process p = new Process();

                System.Diagnostics.ProcessStartInfo start = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = @"C:\Python312\python.exe",
                    Arguments = $@"-u C:\Users\xuedo\OneDrive\Desktop\UCSC-Keysight\api\orchestrator.py {deviceInfo.Text} {category.Text}",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    RedirectStandardInput = true
                };

                p.StartInfo = start;
                p.EnableRaisingEvents = true;

                StringBuilder outputBuilder;

                p.Start();
                //p.BeginOutputReadLine();
                MessageBox.Show(p.StandardOutput.ReadToEnd());
                p.WaitForExit();
            }
        }
    }
}
