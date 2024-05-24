from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A Power Supply", "An OpenTAP plugin for the Keysight EDU36311A Triple Output Programmable DC Power Supply.", "Power Supplies"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def SetVoltage(self, channel, voltage):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")
    
    def SetCurrent(self, channel, current):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"CURR {current}")
    
    def OutputOn(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP ON")
    
    def OutputOff(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP OFF")
    
    def MeasureVoltage(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        return self.querySCPI(Double, "MEAS:VOLT?")
    
    def MeasureCurrent(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        return self.querySCPI(Double, "MEAS:CURR?")
    
    def opc(self):
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            time.sleep(0.1)
            complete = self.ScpiQuery[Double]('*OPC?')

    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result