from opentap import *
import OpenTap
from System import String

from .E8363BAnalyzer import AnalyzerE8363B

@attribute(OpenTap.Display("Configure Frequency Range", "Configures the frequency range of the Analyzer E8363B.", "Frequency Settings"))
class ConfigureFrequencyRange(TestStep):
    Instrument = property(AnalyzerE8363B, None).add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))
    StartFrequency = property(Double, 1e6).add_attribute(OpenTap.Display("Start Frequency (Hz)", "Start frequency in hertz.", "Frequency Settings"))
    StopFrequency = property(Double, 1e9).add_attribute(OpenTap.Display("Stop Frequency (Hz)", "Stop frequency in hertz.", "Frequency Settings"))
    Resolution = property(Double, 1e3).add_attribute(OpenTap.Display("Resolution (Hz)", "Frequency resolution in hertz.", "Frequency Settings"))

    def __init__(self):
        super(ConfigureFrequencyRange, self).__init__()
        self.Name = "Configure Frequency Range"

    def Run(self):
        super().Run()
        
        self.Instrument.normalSCPI(f'CONFigure:FREQuency:STARt {self.StartFrequency}')
        self.Instrument.normalSCPI(f'CONFigure:FREQuency:STOP {self.StopFrequency}')
        self.Instrument.normalSCPI(f'CONFigure:FREQuency:RESolution {self.Resolution}')
        
        self.UpgradeVerdict(OpenTap.Verdict.Pass)