from opentap import *
from System import Double, String
import OpenTap

@attribute(OpenTap.Display("Analyzer E8363B", "A SCPI instrument driver for the Analyzer E8363B.", "Network Analyzers"))
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

    def setup_measurement(self, measurement_type):
        self.normalSCPI(f":CALCulate1:PARameter:DEFine:EXTended '{measurement_type}',S21")
        self.normalSCPI(f":DISPlay:WINDow1:STATe ON")
        self.normalSCPI(f":DISPlay:WINDow1:TRACe1:FEED '{measurement_type}'")
    
    def set_frequency_range(self, start_freq, stop_freq):
        self.normalSCPI(f":SENSe1:FREQuency:STARt {start_freq}")
        self.normalSCPI(f":SENSe1:FREQuency:STOP {stop_freq}")
    
    def set_sweep_points(self, points):
        self.normalSCPI(f":SENSe1:SWEep:POINts {points}")
    
    def perform_single_sweep(self):
        self.normalSCPI(":SENSe1:SWEep:MODE SINGle")
        self.opc()
    
    def fetch_data(self):
        self.normalSCPI(":FORMat:DATA ASCii")
        return self.querySCPI(String, ":CALCulate1:DATA? SDATA")
    
    def opc(self):
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[Double]('*OPC?')
    
    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result