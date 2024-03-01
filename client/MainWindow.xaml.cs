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
            if (deviceInfo != null && category != null &&
                !string.IsNullOrWhiteSpace(deviceInfo.Text) && !string.IsNullOrWhiteSpace(category.Text))
            {
                MessageBox.Show($@"C:\Users\shaun\Desktop\UCSC-Keysight\api\.py {deviceInfo.Text} {category.Text}");

                System.Diagnostics.ProcessStartInfo start = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = @"C:\Users\shaun\AppData\Local\Microsoft\WindowsApps\python3.exe",
                    Arguments = $@"C:\Users\shaun\Desktop\UCSC-Keysight\api\.py {deviceInfo.Text} {category.Text}",
                    UseShellExecute = false,
                    RedirectStandardOutput = true
                };

                using (System.Diagnostics.Process process = System.Diagnostics.Process.Start(start))
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
