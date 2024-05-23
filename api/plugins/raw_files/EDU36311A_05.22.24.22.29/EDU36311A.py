from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("Keysight EDU36311A Power Supply", "A SCPI instrument driver for the Keysight EDU36311A Power Supply.", "Power Supply"))
class EDU36311A(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311A, self).__init__()
        self.log = Trace(self)
        self.Name = "Keysight EDU36311A Power Supply"
    
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")
    
    def Reset(self):
        self.ScpiCommand("*RST")
    
    def SetVoltage(self, channel, voltage):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        self.ScpiCommand(f"VOLT {voltage}")
    
    def SetCurrent(self, channel, current):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        self.ScpiCommand(f"CURR {current}")
    
    def OutputOn(self, channel):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        self.ScpiCommand("OUTP ON")
    
    def OutputOff(self, channel):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        self.ScpiCommand("OUTP OFF")
    
    def MeasureVoltage(self, channel):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        return self.ScpiQuery[float]("MEAS:VOLT?")
    
    def MeasureCurrent(self, channel):
        self.ScpiCommand(f"INST:SEL CH{channel}")
        return self.ScpiQuery[float]("MEAS:CURR?")
    
    def opc(self):
        complete = self.ScpiQuery[int]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[int]('*OPC?')
    
    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result