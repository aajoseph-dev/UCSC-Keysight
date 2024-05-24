Based on the context provided, here is an OpenTAP plugin class that includes a function to enable the display of the Keysight EDU36311A Triple Output Programmable DC Power Supply. I have used the provided example code and instructions to craft a class that fits into the OpenTAP architecture.

```python
import sys
import opentap
import clr
clr.AddReference("System")
from System import String, Double
import OpenTap
from OpenTap import TestStep, Trace, attribute, Display

# Here is how a test step plugin is defined: 

# Use the Display attribute to define how the test step should be presented to the user.
@attribute(Display("EDU36311A Power Supply", "An OpenTAP plugin for the Keysight EDU36311A Triple Output Programmable DC Power Supply.", "Power Supplies"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):

    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"

    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")

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

    def MeasureVoltage(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        return self.querySCPI(Double, "MEAS:VOLT?")

    def MeasureCurrent(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        return self.querySCPI(Double, "MEAS:CURR?")

    def EnableDisplay(self):
        # Assuming that enabling the display is done with the DISP command
        # This is a placeholder; actual command to enable display should be replaced here
        self.normalSCPI("DISP ON")

    def opc(self):
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            time.sleep(0.1)
            complete = self.ScpiQuery[Double]('*OPC?')

    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()

    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result
```

Please note that the actual SCPI command to enable the display for the EDU36311A Power Supply is not provided in the context, so I have used `"DISP ON"` as a placeholder. You should replace this with the correct SCPI command according to the programming guide of the device.

Additionally, this class assumes that the user has already configured the communication interface to connect to the device using the correct USB address. The OpenTAP framework allows for such configurations to be set up in the Test Plan or in the Settings of the Instrument resource.

Remember to refer to the Keysight EDU36311A Triple Output Programmable DC Power Supply Programming Guide for the exact SCPI commands needed to operate the device.