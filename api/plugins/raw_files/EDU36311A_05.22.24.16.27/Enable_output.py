Based on your instructions and the example code provided, here is a Python class that can be used as an OpenTAP plugin for the Keysight EDU36311A Triple Output Programmable DC Power Supply. This class includes functions to enable and disable the output as per the SCPI commands, set voltage and current, and measure voltage and current.

```python
from opentap import *
from System import String, Double

@attribute(Display("EDU36311A", "Keysight Triple Output Programmable DC Power Supply Instrument Driver", "Generator EDU36311A"))
class EDU36311A(ScpiInstrument):
    
    def __init__(self):
        super(EDU36311A, self).__init__()
        self.Name = "EDU36311A"
    
    def GetIdnString(self):
        idn = self.ScpiQuery[String]("*IDN?")
        return idn
    
    def reset(self):
        self.ScpiCommand("*RST")
        self.WaitForOpc()
    
    def setVoltage(self, channel, voltage):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"VOLT {voltage}")
        self.WaitForOpc()
    
    def setCurrent(self, channel, current):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand(f"CURR {current}")
        self.WaitForOpc()
    
    def outputOn(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand("OUTP ON")
        self.WaitForOpc()
    
    def outputOff(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        self.ScpiCommand("OUTP OFF")
        self.WaitForOpc()
    
    def measureVoltage(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        voltage = self.ScpiQuery[Double]("MEAS:VOLT?")
        self.WaitForOpc()
        return voltage
    
    def measureCurrent(self, channel):
        self.ScpiCommand(f"INST:NSEL {channel}")
        current = self.ScpiQuery[Double]("MEAS:CURR?")
        self.WaitForOpc()
        return current
    
    def WaitForOpc(self):
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[Double]('*OPC?')
```

This class is a template and provides the basic functionality for the EDU36311A device. Each method corresponds to a specific SCPI command. For instance, `outputOn` and `outputOff` enable and disable the device's output, respectively, while `setVoltage` and `setCurrent` set the voltage and current for a specified channel. The `WaitForOpc` method is used to ensure that the device has completed the previous command before continuing.

Please note that this is a simplified version and additional error handling, input validation, and other features might be needed depending on the actual requirements of your application. Also, you will need to instantiate this class and use it within an OpenTAP Test Plan, including it in Test Steps or as part of a larger sequence of operations.