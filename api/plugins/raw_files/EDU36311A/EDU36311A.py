from opentap import *
from System import Double, String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A Power Supply", "A driver for controlling the EDU36311A Power Supply via SCPI commands.", "Power Supplies"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.ScpiCommand("*RST")
        self.opc()
    
    def setVoltage(self, channel, voltage):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"SOUR:VOLT {voltage}")
        self.opc()
    
    def setCurrent(self, channel, current):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"SOUR:CURR {current}")
        self.opc()
    
    def outputOn(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand("OUTP ON")
        self.opc()
    
    def outputOff(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand("OUTP OFF")
        self.opc()
    
    def measureVoltage(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        measured_voltage = self.ScpiQuery[Double]("MEAS:VOLT?")
        return measured_voltage
    
    def measureCurrent(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        measured_current = self.ScpiQuery[Double]("MEAS:CURR?")
        return measured_current
    
    def opc(self):
        complete = self.ScpiQuery[Double]("*OPC?")
        while complete != 1:
            complete = self.ScpiQuery[Double]("*OPC?")
    
    def ScpiCommand(self, command):
        self.SendScpiCommand(command)
        self.opc()
    
    def ScpiQuery(self, format, query):
        result = self.QueryScpi(format, query)
        self.opc()
        return result