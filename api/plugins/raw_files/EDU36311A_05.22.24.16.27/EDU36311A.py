from opentap import *
from System import String, Double
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A", "Keysight Triple Output Programmable DC Power Supply Instrument Driver", "Generator EDU36311A"))
class EDU36311A(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311A, self).__init__()
        self.Name = "EDU36311A"
        self.log = Trace(self)
    
    def GetIdnString(self):
        idn = self.ScpiQuery[String]("*IDN?")
        return idn
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def setVoltage(self, channel, voltage):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")
    
    def setCurrent(self, channel, current):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"CURR {current}")
    
    def outputOn(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP ON")
    
    def outputOff(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP OFF")
    
    def measureVoltage(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        voltage = self.querySCPI(Double, "MEAS:VOLT?")
        return voltage
    
    def measureCurrent(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        current = self.querySCPI(Double, "MEAS:CURR?")
        return current
    
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