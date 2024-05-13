import opentap
from opentap import *
from System import String
import visa
import numpy as np

# Import the OpenTAP Python library
from OpenTap import DisplayAttribute, Instrument

# Define the plugin class
@attribute(DisplayAttribute, "EDU36311A Power Supply", "Plugin for EDU36311A power supply to measure voltage, current, and power.", "Power Supply")
class EDU36311APowerSupply(Instrument):
    def __init__(self):
        super().__init__()
        self.Name = "EDU36311A"
        self._resource_manager = visa.ResourceManager()
        self._instrument = None

    def Open(self):
        # Open the connection to the power supply using the VISA resource manager
        super().Open()
        self._instrument = self._resource_manager.open_resource("USB0::0x2A8D::0x1202::MY1234567::INSTR")
        
    def Close(self):
        # Close the connection to the power supply
        if self._instrument is not None:
            self._instrument.close()
        super().Close()

    @method(String)
    def MeasureVoltage(self):
        # Measure the output voltage
        return self._instrument.query("MEAS:VOLT?")

    @method(String)
    def MeasureCurrent(self):
        # Measure the output current
        return self._instrument.query("MEAS:CURR?")

    @method(String)
    def MeasurePower(self):
        # Measure the output power
        return self._instrument.query("MEAS:POW?")

# Register the plugin with OpenTAP
Instrument.Add(EDU36311APowerSupply)