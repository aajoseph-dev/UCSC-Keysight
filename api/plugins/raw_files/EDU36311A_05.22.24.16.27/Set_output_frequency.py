The provided example code is for a different type of device (an oscilloscope, it seems) and for different operations. However, we can use it as a template for the structure and flow of an OpenTAP plugin in Python. Below is the OpenTAP plugin class for the EDU36311A power supply that includes functions for setting the output frequency via SCPI commands:

```python
import sys
import opentap
import clr
from opentap import *

import OpenTap
from OpenTap import Log, AvailableValues, EnabledIfAttribute

# Import necessary .NET APIs
import System
from System import String, Double

# Here is how an instrument plugin is defined:

# Use the Display attribute to define how the instrument should be presented to the user.
@attribute(OpenTap.Display("EDU36311A", "Keysight Triple Output Programmable DC Power Supply Instrument Driver", "Generator EDU36311A"))
class EDU36311A(OpenTap.ScpiInstrument):

    def __init__(self):
        super(EDU36311A, self).__init__()
        self.Name = "EDU36311A"
        self.log = Trace(self)
    
    def GetIdnString(self):
        idn = self.ScpiQuery[String]("*IDN?")
        return idn
    
    def reset(self):
        self.ScpiCommand("*RST")
        self.opc()
    
    def setOutputFrequency(self, channel, frequency):
        # This command sets the output frequency for a given channel
        # Assuming that 'FREQ' is the appropriate SCPI command for setting frequency
        self.ScpiCommand(f"INST:NSEL {channel};:FREQ {frequency}")
        self.opc()
    
    def outputOn(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel};:OUTP ON")
        self.opc()
    
    def outputOff(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel};:OUTP OFF")
        self.opc()
    
    def opc(self):
        # Operation complete query
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[Double]('*OPC?')

    # Add other methods to interact with the instrument as needed

# If you have additional steps that utilize this instrument, you can define them similarly:
@attribute(OpenTap.Display("Set Output Frequency", "Sets the output frequency of the EDU36311A power supply.", "Generator EDU36311A"))
class SetOutputFrequencyStep(TestStep):
    Instrument = property(EDU36311A, None).add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))
    Channel = property(int, 1).add_attribute(OpenTap.Display("Channel", "Select the output channel.", "Parameter", 2))
    Frequency = property(double, 1000.0).add_attribute(OpenTap.Display("Frequency", "Set the output frequency.", "Parameter", 3))

    def __init__(self):
        super(SetOutputFrequencyStep, self).__init__()
    
    def Run(self):
        super().Run()
        self.Instrument.setOutputFrequency(self.Channel, self.Frequency)
        self.UpgradeVerdict(OpenTap.Verdict.Pass)
```

Please note that this plugin assumes that the SCPI command for setting the frequency is `FREQ`. However, since the provided documentation does not include the specific SCPI commands for the EDU36311A, you'll need to consult the programming guide for the exact command and adjust the code accordingly.

Remember to always test the plugin with the actual hardware to ensure proper functionality and to handle any device-specific quirks or requirements.