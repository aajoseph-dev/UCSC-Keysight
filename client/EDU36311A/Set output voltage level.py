import OpenTap
from OpenTap import *
from System import String, Double

@attribute(Display("EDU36311 Power Supply", "An example SCPI instrument driver for the EDU36311 Power Supply.", "EDU36311"))
class PowerSupplyEDU36311(ScpiInstrument):

    def __init__(self):
        super(PowerSupplyEDU36311, self).__init__()
        self.Name = "EDU36311"
    
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def setVoltageImmediate(self, voltage):
        self.normalSCPI(f"VOLT {voltage}")
    
    def setVoltageTriggered(self, voltage):
        self.normalSCPI(f"VOLT:TRIG {voltage}")
    
    def queryVoltageImmediate(self):
        return self.querySCPI(Double, "VOLT?")
    
    def queryVoltageTriggered(self):
        return self.querySCPI(Double, "VOLT:TRIG?")
    
    def setVoltageMode(self, mode):
        # mode should be either "FIX" for fixed mode or "STEP" for step mode
        self.normalSCPI(f"VOLT:MODE {mode}")
    
    def setOverVoltageProtection(self, voltage):
        self.normalSCPI(f"VOLT:PROT {voltage}")
    
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