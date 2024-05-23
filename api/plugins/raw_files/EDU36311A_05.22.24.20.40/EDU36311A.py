from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A Power Supply", "OpenTAP Instrument Driver for Keysight EDU36311A Power Supply.", "Power Supplies"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        idn = self.ScpiQuery[String]("*IDN?")
        return idn
    
    def reset(self):
        self.normalSCPI("*RST")
    
    def SetVoltage(self, channel, voltage):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")
    
    def SetCurrent(self, channel, current):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"CURR {current}")
    
    def OutputOn(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP ON")
    
    def OutputOff(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP OFF")
    
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

# Example usage:
# power_supply = EDU36311APowerSupply()
# power_supply.Initialize()
# power_supply.SetVoltage(1, 5.0) # Set 5V on channel 1
# power_supply.SetCurrent(1, 0.5) # Set 0.5A on channel 1
# power_supply.OutputOn(1) # Turn on channel 1
# power_supply.reset() # Reset the power supply to factory defaults
# power_supply.Close()