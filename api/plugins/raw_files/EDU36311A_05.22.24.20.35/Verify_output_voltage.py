Below is the code for an OpenTAP plugin class tailored to control a Keysight EDU36311A Triple Output Programmable DC Power Supply. The class includes methods for setting voltages, currents, turning outputs on and off, measuring voltages and currents, enabling tracking mode, and verifying tracking between outputs.

Please note that Python does not support decorators with attributes in the same way as C#, so `@attribute` usage has been modified to Python comments as placeholders for where you would put attributes in C#.

```python
import OpenTap
from OpenTap import *
from System import String, Double

# Placeholder for OpenTAP Display attribute
# @attribute(OpenTap.Display("EDU36311A", "Keysight Triple Output Programmable DC Power Supply", "Power Supplies"))
class EDU36311APowerSupply(ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
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
        voltage = self.ScpiQuery[Double](f"MEAS:VOLT? (@{channel})")
        return voltage
    
    def MeasureCurrent(self, channel):
        current = self.ScpiQuery[Double](f"MEAS:CURR? (@{channel})")
        return current
    
    def EnableTrackingMode(self):
        self.ScpiCommand("OUTP:TRAC ON")
    
    def VerifyTracking(self, channel1, channel2):
        # Measure the voltage of both channels
        voltage1 = self.MeasureVoltage(channel1)
        voltage2 = self.MeasureVoltage(channel2)
        
        # Verify if the voltages are the same
        if voltage1 == voltage2:
            self.log.Info(f"Output {channel1} and Output {channel2} are properly tracking.")
            return True
        else:
            self.log.Error(f"Output {channel1} and Output {channel2} are not tracking properly.")
            return False

# Placeholder for OpenTAP TestStep attribute
# @attribute(OpenTap.TestStep())
class VerifyOutputVoltageStep(TestStep):
    # Placeholder for OpenTAP Display attribute
    # @attribute(OpenTap.Display("Verify Output Voltage", "Verify that the output voltage of channel 2 and 3 are tracking.", "EDU36311A Power Supply"))
    def __init__(self):
        super(VerifyOutputVoltageStep, self).__init__()
        self.powerSupply = None
    
    def Run(self):
        self.powerSupply.EnableTrackingMode()
        if self.powerSupply.VerifyTracking(2, 3):
            self.UpgradeVerdict(Verdict.Pass)
        else:
            self.UpgradeVerdict(Verdict.Fail)

# Instantiate and use the class in an OpenTAP test plan
ps = EDU36311APowerSupply()
ps.ResourceName = "ASRL::INSTR"  # Set the VISA resource name for your instrument
ps.Open()
