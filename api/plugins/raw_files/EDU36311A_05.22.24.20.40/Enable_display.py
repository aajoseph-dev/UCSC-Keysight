Based on the given context, I'll create a Python class for an OpenTAP plugin for the Keysight EDU36311A Power Supply that includes the SCPI command to enable the display. I'll assume the SCPI command for enabling the display is `DISP:ENAB`, which is a common pattern but not guaranteed without the specific documentation for this model.

Please note that the provided example code seems to be a mix of Python and C# syntax, which is not directly compatible. The OpenTAP Python SDK would allow you to write test steps and instrument drivers in Python. However, the given example code is more aligned with C# syntax used in OpenTAP C# SDK. I will follow the style of the example code, but please be aware that in a real-world scenario, you should consult the OpenTAP Python SDK documentation for the exact syntax and usage.

```python
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
    
    # Existing methods from the example code
    # ...

    def EnableDisplay(self):
        self.normalSCPI("DISP:ENAB")
        self.log.Info("Display enabled.")

    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def opc(self):
        complete = False
        while not complete:
            complete = self.ScpiQuery[bool]("*OPC?")
            time.sleep(0.1)

# Example usage:
# power_supply = EDU36311APowerSupply()
# power_supply.Initialize()
# power_supply.EnableDisplay() # Enable the display on the power supply
# power_supply.Close()
```

In this code snippet, I've added the `EnableDisplay` method to the `EDU36311APowerSupply` class, which sends the `DISP:ENAB` command to the device. The `normalSCPI` method is used to send SCPI commands and wait for operation complete using the `opc` method.

Remember, the actual SCPI command to enable the display could be different for the EDU36311A, and you would need to refer to the device's programming guide for the exact command.

The `opc` method checks if the previous command has been completed before moving on. This is done by querying the `*OPC?` command repeatedly until a `True` response is received, indicating the completion.

The example usage shows how to create an instance of the `EDU36311APowerSupply` class, initialize the instrument, enable the display, and then close the connection to the instrument.

Please ensure you have the OpenTAP Python SDK properly installed and configured in your environment to use this code, and adapt it as needed to fit the actual command set of your device.