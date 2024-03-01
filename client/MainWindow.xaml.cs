using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;

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
            if (deviceInfo != null && !string.IsNullOrWhiteSpace(deviceInfo.Text))
            {
                MessageBox.Show(deviceInfo.Text);

                ProcessStartInfo start = new ProcessStartInfo
                {
                    FileName = @"C:\Users\shaun\AppData\Local\Microsoft\WindowsApps\python3.exe",
                    Arguments = @"C:\Users\shaun\Desktop\UCSC-Keysight\api\test.py",
                    UseShellExecute = false,
                    RedirectStandardOutput = true
                };

                using (Process process = Process.Start(start))
                {
                    if (process != null)
                    {
                        using (StreamReader reader = process.StandardOutput)
                        {
                            if (reader != null)
                            {
                                string result = reader.ReadToEnd();
                                MessageBox.Show(result);
                            }
                        }
                    }
                }
            }
        }
    }
}
