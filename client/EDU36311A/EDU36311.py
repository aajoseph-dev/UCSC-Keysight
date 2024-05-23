from opentap import *
from System import Double, String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311 Power Supply", "An example SCPI instrument driver for the EDU36311 Power Supply.", "EDU36311"))
class PowerSupplyEDU36311(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(PowerSupplyEDU36311, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311"
    
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def setVoltage(self, voltage):
        self.normalSCPI(f"VOLT {voltage}")
    
    def setCurrent(self, current):
        self.normalSCPI(f"CURR {current}")
    
    def outputOn(self):
        self.normalSCPI("OUTP ON")
    
    def outputOff(self):
        self.normalSCPI("OUTP OFF")
    
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