import OpenTap
from OpenTap import *
from System import String, Double

@attribute(Display("EDU36311A Power Supply", "A driver for controlling the EDU36311A Power Supply via SCPI commands.", "Power Supplies"))
class EDU36311APowerSupply(ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.Name = "EDU36311A Power Supply"

    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.ScpiCommand("*RST")
        self.opc()

    # Function to enable the display of the power supply
    def EnableDisplay(self):
        self.ScpiCommand("DISP:ENAB")
        self.opc()

    # Other existing functions...

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