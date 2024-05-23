from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("EDU36311A", "Keysight Triple Output Programmable DC Power Supply", "Power Supplies"))
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
        
    def SetVoltage(self, channel, voltage):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"VOLT {voltage}")
        
    def SetCurrent(self, channel, current):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"CURR {current}")
        
    def OutputOn(self, channel):
        self.ScpiCommand(f"OUTP:SEL {channel}")
        self.ScpiCommand("OUTP ON")
        
    def OutputOff(self, channel):
        self.ScpiCommand(f"OUTP:SEL {channel}")
        self.ScpiCommand("OUTP OFF")
        
    def MeasureVoltage(self, channel):
        self.ScpiCommand(f"MEAS:VOLT? (@" + str(channel) + ")")
        measured_voltage = self.ScpiQuery[Double]()
        return measured_voltage
        
    def MeasureCurrent(self, channel):
        self.ScpiCommand(f"MEAS:CURR? (@" + str(channel) + ")")
        measured_current = self.ScpiQuery[Double]()
        return measured_current
    
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