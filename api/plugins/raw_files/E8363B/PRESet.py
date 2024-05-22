import opentap
from opentap import *
from System import String
import visa

@attribute(DisplayAttribute, "E8363B Network Analyzer", "SCPI-controlled Network Analyzer", "Instrumentation")
class NetworkAnalyzerE8363B(Instrument):
    def __init__(self):
        super().__init__()  # The base class initializer must be invoked.
        self._resource_manager = visa.ResourceManager()
        self._instrument = None
        self.Name = "E8363B Network Analyzer"
        self.Address = "GPIB0::16::INSTR"  # Default VISA address, update as needed.

    def Open(self):
        try:
            self._instrument = self._resource_manager.open_resource(self.Address)
            super().Open()
            self.Log.Info(f"{self.Name} connected at {self.Address}")
        except visa.VisaIOError as e:
            self.Log.Error(f"Failed to connect to {self.Name} at {self.Address}: {e}")

    def Close(self):
        if self._instrument is not None:
            self._instrument.close()
        super().Close()
        self.Log.Info(f"{self.Name} disconnected")

    @method()
    def SaveUserPreset(self):
        """ Saves the current state as the user preset state. """
        if self._instrument is None:
            self.Log.Error("Instrument is not connected.")
            return
        self._instrument.write(":SYST:PRES:USER:SAVE")
        self.Log.Info("User Preset state saved.")

    @method()
    def RecallUserPreset(self):
        """ Recalls the user preset state. """
        if self._instrument is None:
            self.Log.Error("Instrument is not connected.")
            return
        self._instrument.write(":SYST:PRES:USER")
        self.Log.Info("User Preset state recalled.")

    @method()
    def SystemPreset(self):
        """ Returns the signal generator to a set of defined conditions for the current mode. """
        if self._instrument is None:
            self.Log.Error("Instrument is not connected.")
            return
        self._instrument.write(":SYST:PRESet")
        self.Log.Info("System Preset executed.")

# Example of how to use the plugin
if __name__ == "__main__":
    # Instantiate the instrument
    na = NetworkAnalyzerE8363B()
    # Set the VISA address if different from the default
    na.Address = "Your VISA Address Here"
    
    # Open the instrument connection
    na.Open()
    
    # Perform operations
    try:
        na.SaveUserPreset()
        na.RecallUserPreset()
        na.SystemPreset()
    finally:
        # Close the instrument connection
        na.Close()