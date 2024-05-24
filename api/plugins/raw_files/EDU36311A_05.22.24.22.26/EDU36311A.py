from opentap import *
from System import String
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A Power Supply", "SCPI instrument driver for the EDU36311A Triple Output Programmable DC Power Supply.", "Keysight EDU36311A"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def reset(self):
        self.normalSCPI("*RST")

    # Additional methods to control the power supply should be added here.
    # For example, methods to set voltage, current, output on/off, etc.

    def setVoltage(self, channel, voltage):
        # Assuming channel is 1, 2 or 3 and voltage is a float.
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")

    def setCurrent(self, channel, current):
        # Assuming channel is 1, 2 or 3 and current is a float.
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"CURR {current}")

    def outputOn(self, channel):
        # Assuming channel is 1, 2 or 3.
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP ON")

    def outputOff(self, channel):
        # Assuming channel is 1, 2 or 3.
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP OFF")

    def opc(self):
        complete = self.ScpiQuery[String]('*OPC?')
        while complete != "1":
            complete = self.ScpiQuery[String]('*OPC?')

    def normalSCPI(self, scpi_command):
        self.ScpiCommand(scpi_command)
        self.opc()

    # Additional query methods can be added here to retrieve data from the power supply.

# Example usage
if __name__ == "__main__":
    power_supply = EDU36311APowerSupply()
    power_supply.Open()
    power_supply.reset()
    print(power_supply.GetIdnString())
    power_supply.setVoltage(1, 5.0)  # Set 5V on channel 1
    power_supply.setCurrent(1, 1.0)  # Set 1A current limit on channel 1
    power_supply.outputOn(1)         # Turn on channel 1 output
    time.sleep(10)                   # Wait for 10 seconds
    power_supply.outputOff(1)        # Turn off channel 1 output
    power_supply.Close()