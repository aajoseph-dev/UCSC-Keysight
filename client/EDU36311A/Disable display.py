import OpenTap
from OpenTap import *
from System import String, Double, Boolean

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
    
    def queryVoltageImmediate(self):
        return self.querySCPI(Double, "VOLT?")
    
    def outputOn(self):
        self.normalSCPI("OUTP ON")
    
    def outputOff(self):
        self.normalSCPI("OUTP OFF")
    
    def enableDisplay(self, enable):
        # enable should be a boolean value: True to enable, False to disable
        value = 'ON' if enable else 'OFF'
        self.normalSCPI(f":DISP:ENAB {value}")
    
    def queryDisplayEnabled(self):
        # Returns True if display is enabled, False if disabled
        return self.querySCPI(Boolean, ":DISP:ENAB?") == 1
    
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