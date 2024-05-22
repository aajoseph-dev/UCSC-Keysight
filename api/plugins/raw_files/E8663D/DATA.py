import opentap
from opentap import *
from System import String
import visa

@attribute(DisplayAttribute, "E8663D PSG Signal Generator", "SCPI Plugin for E8663D PSG Signal Generator", "Instrumentation")
class E8663DSignalGenerator(Instrument):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.Name = "E8663D PSG Signal Generator"
        self._visa_resource_manager = visa.ResourceManager()
        self._instrument = None

    def Open(self):
        super().Open()
        # This is where you would open the connection to the instrument
        resource_name = "GPIB0::20::INSTR"  # Example VISA address, replace with actual address
        self._instrument = self._visa_resource_manager.open_resource(resource_name)

    def Close(self):
        # This is where you would close the connection to the instrument
        if self._instrument is not None:
            self._instrument.close()
        super().Close()

    def send_scpi_command(self, command):
        self._instrument.write(command)

    def query_scpi_command(self, command):
        return self._instrument.query(command)

    @method()
    def EnterSecureMode(self):
        """Enters secure mode and overwrites memory with random characters."""
        self.send_scpi_command(":SYSTem:SECurity:OVERwrite")

    @method()
    def SanitizeMemory(self):
        """Sanitizes memory by overwriting with a single character and then with random characters."""
        self.send_scpi_command(":SYSTem:SECurity:SANitize")

    @method(None, [String])
    def SetScreenSaverDelay(self, delay):
        """
        Sets the screen saver delay.
        :param delay: Delay time in hours before the screen saver activates.
        """
        self.send_scpi_command(f":SYSTem:SSAVer:DELay {delay}")

# Ensure the plugin is discovered by OpenTAP
InstrumentProvider.RegisterInstrument(E8663DSignalGenerator)