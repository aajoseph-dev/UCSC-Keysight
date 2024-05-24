from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A", "A SCPI instrument driver for the Keysight EDU36311A Power Supply", "EDU36311A Power Supply"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def SetVoltage(self, channel, voltage):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")
    
    def SetCurrent(self, channel, current):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"CURR {current}")
    
    def MeasureVoltage(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        voltage = self.querySCPI(float, "MEAS:VOLT?")
        return voltage
    
    def MeasureCurrent(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        current = self.querySCPI(float, "MEAS:CURR?")
        return current
    
    def opc(self):
        complete = False
        while not complete:
            complete = self.ScpiQuery[bool]("*OPC?")
            time.sleep(0.1)
    
    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result