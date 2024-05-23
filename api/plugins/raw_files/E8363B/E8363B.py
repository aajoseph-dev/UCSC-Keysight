from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("E8363B Analyzer", "SCPI instrument driver for the E8363B PNA Network Analyzer.", "E8363B"))
class E8363BAnalyzer(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(E8363BAnalyzer, self).__init__()
        self.log = Trace(self)
        self.Name = "E8363B"

    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string

    def reset(self):
        self.normalSCPI("*RST")

    def setup_measurement(self, measurement_type):
        self.normalSCPI(f"CALCulate1:PARameter:SDEFine 'Meas1', '{measurement_type}'")
        self.normalSCPI("DISPlay:WINDow1:STATe ON")
        self.normalSCPI("DISPlay:WINDow1:TRACe1:FEED 'Meas1'")

    def set_frequency_range(self, start_freq, stop_freq):
        self.normalSCPI(f"SENSe:FREQuency:STARt {start_freq}")
        self.normalSCPI(f"SENSe:FREQuency:STOP {stop_freq}")

    def set_sweep_points(self, points):
        self.normalSCPI(f"SENSe:SWEep:POINts {points}")

    def trigger_single_sweep(self):
        self.normalSCPI("INITiate1:CONTinuous OFF")
        self.normalSCPI("INITiate1:SINGle")

    def fetch_data(self):
        data_string = self.querySCPI(String, "CALCulate1:DATA? SDATA")
        return data_string

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