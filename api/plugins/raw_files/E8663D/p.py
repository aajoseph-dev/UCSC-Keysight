Below is a Python OpenTAP plugin class for the E8663D generator that implements a subset of SCPI commands for controlling output power and querying the current hostname. The plugin class is designed to be used with OpenTAP and does not rely on visa or pyvisa for instrument communication.

```python
import opentap
from opentap import *
from System import String

# Define the plugin class
@attribute(Display("E8663D Generator SCPI Control", "Plugin to control E8663D generator using SCPI commands.", "SCPI"))
class E8663DGeneratorSCPIControl(TestStep):
    # Define properties required for the SCPI communication
    GPIBAddress = property(int, 1).add_attribute(Display("GPIB Address", "GPIB address of the E8663D Generator", "Communication", 1))

    def __init__(self):
        super(E8663DGeneratorSCPIControl, self).__init__()
        self.Name = "E8663D Generator SCPI Control"
        self.GPIBAddress = 1  # Default GPIB address

    def Run(self):
        super().Run()

        # Establish communication with the instrument
        instrument = Instrument("GPIB0::{}::INSTR".format(self.GPIBAddress))

        try:
            # Query the current hostname
            hostname = instrument.Query(":SYSTem:COMMunicate:ETHernet:HOSTname:CURRent?")
            self.log.Info("Hostname: " + hostname)

            # Set output power value
            power_value = "0 DBM"  # Example power value to set, change as needed
            instrument.Write(":OUTPut:POWer {}".format(power_value))

            # Calculate and store the power offset
            slot = 4  # Example slot number, change as needed
            channel = 4  # Example channel number, change as needed
            instrument.Write(":OUTPut:POWer:OFFSet:POWermeter {},{}".format(slot, channel))

            # Set reference power value
            reference_power_value = "0 DBM"  # Example reference power value to set, change as needed
            instrument.Write(":OUTPut:POWer:REFerence {}".format(reference_power_value))

            # Set verdict
            self.UpgradeVerdict(Verdict.Pass)
        except Exception as e:
            self.log.Error("SCPI command error: " + str(e))
            self.UpgradeVerdict(Verdict.Fail)

# This class represents the instrument and handles SCPI communication.
class Instrument:
    def __init__(self, address):
        self.address = address
        self.log = Log.Create()

    def Write(self, command):
        # Placeholder for instrument write operation
        self.log.Info("SCPI Write: " + command)
        # Here, you would implement the actual communication with the instrument

    def Query(self, command):
        # Placeholder for instrument query operation
        self.log.Info("SCPI Query: " + command)
        # In a real implementation, this would return the actual response from the instrument
        # Mock responses for illustrative purposes
        if command == ":SYSTem:COMMunicate:ETHernet:HOSTname:CURRent?":
            return "A-8164B-1234567"
        return "Mocked response"

# Register the plugin with OpenTAP
OpenTap.TapPlugins.Add(E8663DGeneratorSCPIControl())
```

This plugin, `E8663DGeneratorSCPIControl`, includes methods to query the current hostname, set output power value, calculate and store power offset, and set reference power value. The `Instrument` class within the plugin acts as a placeholder for the actual SCPI communication with the instrument. In a production environment, you would replace the placeholder methods with actual GPIB communication code. The plugin is registered with