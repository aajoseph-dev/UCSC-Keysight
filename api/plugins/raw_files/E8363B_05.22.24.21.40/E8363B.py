from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("Analyzer E8363B", "A SCPI instrument driver for the Agilent E8363B PNA Network Analyzer.", "Network Analyzers"))
class AnalyzerE8363B(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(AnalyzerE8363B, self).__init__()
        self.log = OpenTap.Trace(self)
        self.Name = "Analyzer E8363B"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.ScpiCommand("*RST")
    
    def preset(self):
        self.ScpiCommand(":SYST:PRES")
    
    def self_test(self):
        result = self.ScpiQuery[String]("*TST?")
        return result == "0"
    
    def measure_s_parameters(self, channel=1):
        self.ScpiCommand(f"CALC{channel}:PAR:SEL 'CH{channel}_S11_1'")
        s11 = self.ScpiQuery[String](f"CALC{channel}:DATA? SDATA")
        self.ScpiCommand(f"CALC{channel}:PAR:SEL 'CH{channel}_S21_1'")
        s21 = self.ScpiQuery[String](f"CALC{channel}:DATA? SDATA")
        self.ScpiCommand(f"CALC{channel}:PAR:SEL 'CH{channel}_S12_1'")
        s12 = self.ScpiQuery[String](f"CALC{channel}:DATA? SDATA")
        self.ScpiCommand(f"CALC{channel}:PAR:SEL 'CH{channel}_S22_1'")
        s22 = self.ScpiQuery[String](f"CALC{channel}:DATA? SDATA")
        return s11, s21, s12, s22
    
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