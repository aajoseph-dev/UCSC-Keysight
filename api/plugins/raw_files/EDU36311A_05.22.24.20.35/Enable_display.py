Below is an OpenTAP plugin class for the Keysight EDU36311A power supply in Python. This class includes a function to enable the display, which is a subset of the SCPI commands for the device. Note that the example provided uses some placeholder classes like `Scope` and `ADS_setting` which are not relevant for this power supply plugin, so they are omitted.

```python
import OpenTap
from OpenTap import *
from System import String, Double

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
    
    def EnableDisplay(self):
        # Assuming "DISP ON" is the correct SCPI command to enable the display
        self.ScpiCommand("DISP ON")
    
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

# Example usage within a test step
@attribute(OpenTap.Display("Enable Display", "Enable the display of the power supply.", "Power Supply Operations"))
class EnableDisplayTestStep(TestStep):
    # Add properties (name, value, C# type)
    PowerSupply = property(EDU36311APowerSupply, None)\
        .add_attribute(OpenTap.Display("Power Supply", "The power supply to use in the step.", "Resources"))

    def __init__(self):
        super(EnableDisplayTestStep, self).__init__() # The base class initializer must be invoked.

    def Run(self):
        super().Run() ## Required for debugging to work.
        
        # Enable the display of the power supply
        self.PowerSupply.EnableDisplay()
        
        # Set verdict
        self.UpgradeVerdict(OpenTap.Verdict.Pass)

```

Please note that the actual SCPI command for enabling the display is assumed to be "DISP ON" based on the context provided. However, you should verify