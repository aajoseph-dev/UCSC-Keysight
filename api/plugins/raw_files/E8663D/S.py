Below is an example of an OpenTAP plugin class for a subset of SCPI commands for the E8663D Generator device using Python. This class will include functions to utilize the provided SCPI commands without importing visa or pyvisa, but instead using the OpenTAP and other specified libraries.

```python
import opentap
from opentap import *
from System import String
from System.Collections.Generic import List

@attribute(Display("E8663D Generator SCPI Plugin", "Plugin for controlling E8663D Generator using SCPI commands.", "SCPI"))
class E8663DGeneratorSCPI(TestStep):
    # Define properties required for the SCPI communication
    GPIBAddress = property(int, 1).add_attribute(Display("GPIB Address", "GPIB address of the E8663D Generator", "Communication", 1))
    
    def __init__(self):
        super(E8663DGeneratorSCPI, self).__init__()
        self.Name = "E8663D Generator SCPI Plugin"
        self.GPIBAddress = 1  # Default GPIB address

    def Run(self):
        super().Run()
        
        # Establish communication with the instrument
        instrument = Instrument("GPIB0::{}::INSTR".format(self.GPIBAddress))
        
        try:
            # Example of using SCPI commands
            # Send SCPI command to set signal length
            instrument.Write(":SBUS1:SENT:SIGNal1:LENGth 100")
            
            # Example of querying the instrument
            response = instrument.Query(":SBUS1:SENT:SIGNal1:LENGth?")
            self.log.Info("Signal Length: " + response)
            
            # Send SCPI command to set signal offset
            instrument.Write(":SBUS1:SENT:SIGNal1:OFFSet 0.5")
            
            # Example of setting trigger delay
            instrument.Write("TRIG:EXT1:DEL 100 ms")
            
            # Example of setting attenuation speed
            instrument.Write(":INPut1:CHANnel1:ATTenuation:SPEed 2")
            speed_response = instrument.Query(":INPut1:CHANnel1:ATTenuation:SPEed?")
            self.log.Info("Attenuation Speed: " + speed_response)
            
            # Set verdict
            self.UpgradeVerdict(Verdict.Pass)
        except Exception as e:
            self.log.Error("SCPI command error: " + str(e))
            self.UpgradeVerdict(Verdict.Fail)

# This class represents the instrument and handles SCPI communication.
# Normally, you would import a library to handle the communication, but since we are not importing pyvisa, we will define a basic placeholder.
class Instrument:
    def __init__(self, address):
        self.address = address
        self.log = Log.Create()
        
    def Write(self, command):
        # Placeholder for instrument write operation
        self.log.Info("SCPI Write: " + command)
        
    def Query(self, command):
        # Placeholder for instrument query operation
        self.log.Info("SCPI Query: " + command)
        return "Response from " + command

# Register the plugin with OpenTAP
OpenTap.TapPlugins.Add(E8663DGeneratorSCPI())
```

This example demonstrates how to create an OpenTAP plugin class for sending SCPI commands to a generator. The `Instrument` class serves as a placeholder for the actual communication with the instrument, which would typically be handled by a library like pyvisa. The `E8663DGeneratorSCPI` class includes methods for writing and querying SCPI commands to control the generator and retrieve information.

Please replace the placeholder `Instrument` class with actual communication code that fits your environment. If you need to use an external library for GPIB communication, you would need to implement