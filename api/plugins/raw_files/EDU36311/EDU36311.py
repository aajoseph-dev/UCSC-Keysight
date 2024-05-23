from opentap import *
from System import Double, String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311 Power Supply", "SCPI Instrument Driver for EDU36311 Power Supply.", "EDU36311"))
class PowerSupplyEDU36311(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(PowerSupplyEDU36311, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def setVoltage(self, channel, voltage):
        self.normalSCPI(f"INST:SEL CH{channel}")
        self.normalSCPI(f"VOLT {voltage}")
    
    def setCurrent(self, channel, current):
        self.normalSCPI(f"INST:SEL CH{channel}")
        self.normalSCPI(f"CURR {current}")
    
    def measureVoltage(self, channel):
        self.normalSCPI(f"INST:SEL CH{channel}")
        return self.querySCPI(Double, "MEAS:VOLT?")
    
    def measureCurrent(self, channel):
        self.normalSCPI(f"INST:SEL CH{channel}")
        return self.querySCPI(Double, "MEAS:CURR?")
    
    def outputOn(self, channel):
        self.normalSCPI(f"INST:SEL CH{channel}")
        self.normalSCPI("OUTP ON")
    
    def outputOff(self, channel):
        self.normalSCPI(f"INST:SEL CH{channel}")
        self.normalSCPI("OUTP OFF")
    
    def opc(self):
        complete = self.ScpiQuery[Double]("*OPC?")
        while complete != 1:
            complete = self.ScpiQuery[Double]("*OPC?")
    
    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result