from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A", "SCPI driver for the Keysight EDU36311A Triple Output Programmable DC Power Supply.", "Power Supplies"))
class GeneratorEDU36311A(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(GeneratorEDU36311A, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A"
    
    def GetIdnString(self):
        idn = self.ScpiQuery[String]("*IDN?")
        return idn
    
    def Reset(self):
        self.SendScpiCommand("*RST")
    
    # Example method to set voltage on a specific channel
    def SetVoltage(self, channel, voltage):
        self.SendScpiCommand(f"INST:SEL CH{channel}")
        self.SendScpiCommand(f"SOUR:VOLT {voltage}")
    
    # Example method to set current limit on a specific channel
    def SetCurrent(self, channel, current):
        self.SendScpiCommand(f"INST:SEL CH{channel}")
        self.SendScpiCommand(f"SOUR:CURR {current}")
    
    # Example method to turn on a specific channel output
    def OutputOn(self, channel):
        self.SendScpiCommand(f"INST:SEL CH{channel}")
        self.SendScpiCommand("OUTP ON")
    
    # Example method to turn off a specific channel output
    def OutputOff(self, channel):
        self.SendScpiCommand(f"INST:SEL CH{channel}")
        self.SendScpiCommand("OUTP OFF")
    
    # Implement additional methods as needed based on the instrument's capabilities
    
    # Method to wait for operation complete
    def WaitForOperationComplete(self):
        complete = False
        while not complete:
            complete = self.ScpiQuery[bool]("*OPC?")
            time.sleep(0.1) # Add a small delay to prevent overloading the communication bus
    
    # Method to send a SCPI command and wait for operation complete
    def SendScpiCommand(self, command):
        self.ScpiCommand(command)
        self.WaitForOperationComplete()
        
    # Add additional utility methods as needed

# You can add more methods to control the power supply as needed.