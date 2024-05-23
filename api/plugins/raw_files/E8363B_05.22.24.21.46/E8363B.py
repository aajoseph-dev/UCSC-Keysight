from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("Analyzer E8363B", "SCPI Instrument Driver for the E8363B Analyzer.", "Analyzer E8363B"))
class AnalyzerE8363B(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(AnalyzerE8363B, self).__init__()
        self.log = Trace(self)
        self.Name = "Analyzer E8363B"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.normalSCPI("*RST")
    
    # Add additional methods to control and interact with the Analyzer E8363B here
    
    def opc(self):
        complete = self.ScpiQuery[String]('*OPC?')
        while complete != "1":
            complete = self.ScpiQuery[String]('*OPC?')

    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result

# Add additional functions and settings as per the device's capabilities
# For example, you might add methods for setting the frequency range, taking measurements, etc.

# Note: Replace the placeholders with actual SCPI commands for the E8363B Analyzer.