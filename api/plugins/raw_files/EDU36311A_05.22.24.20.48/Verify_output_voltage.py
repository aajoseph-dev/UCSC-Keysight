Based on your description, here's an example of how you could create an OpenTAP plugin class in Python for the EDU36311A power supply that includes the functionality to work with the tracking operation of the device using SCPI commands.

```python
from opentap import *
from System import String, Double
import OpenTap
import time

@attribute(OpenTap.Display("EDU36311A Power Supply", "An OpenTAP plugin for the Keysight EDU36311A Triple Output Programmable DC Power Supply.", "Power Supplies"))
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
    
    def EnableTrackingMode(self):
        self.normalSCPI("OUTP:TRAC ON")
    
    def DisableTrackingMode(self):
        self.normalSCPI("OUTP:TRAC OFF")
    
    def VerifyTracking(self):
        voltage2 = self.MeasureVoltage(2)
        voltage3 = self.MeasureVoltage(3)
        if abs(voltage2 - voltage3) < 0.01:  # Assuming a small tolerance for verification
            self.log.Info("Output 2 and Output 3 are tracking each other properly.")
            return True
        else:
            self.log.Warning("Output 2 and Output 3 are NOT tracking properly.")
            return False
    
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

In this plugin class, I've added methods to:

- Reset the instrument
- Set the voltage and current for each channel
- Turn individual outputs on and off
- Measure voltage and current
- Enable and disable tracking mode
- Verify that the tracking operation is working correctly

The `normalSCPI` and `querySCPI` methods are helper functions that send the SCPI commands and verify operation completion (with `*OPC?`) before proceeding. The `VerifyTracking` function checks if Output 2 and Output 3 are within a specified tolerance, indicating that they are tracking each other correctly.

Please ensure that you have the OpenT