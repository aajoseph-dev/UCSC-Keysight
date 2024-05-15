import opentap
from opentap import *
from System import String, Int32
import visa

@attribute(OpenTap.DisplayAttribute, "EDU36311A Power Supply", "SCPI Plugin for controlling EDU36311A Power Supply", "Power Supply")
class EDU36311APowerSupply(Instrument):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self._visa_resource_manager = visa.ResourceManager()
        self._instrument = None
        self.VisaAddress = property(String, "USB0::0x2A8D::0x1202::MY1234567::INSTR")  # Example VISA address
        self.Channel = property(Int32, 1)  # Default channel number

    def Open(self):
        super().Open()  # Call the base class Open method
        self._instrument = self._visa_resource_manager.open_resource(self.VisaAddress)

    def Close(self):
        if self._instrument is not None:
            self._instrument.close()
        super().Close()  # Call the base class Close method

    def SetChannelDisplay(self, channel, display_on):
        """
        Turns the display of the specified channel on or off.
        :param channel: Channel number (1 to # analog channels)
        :param display_on: True to turn on display, False to turn off
        """
        display_value = 'ON' if display_on else 'OFF'
        command = f":CHANnel{channel}:DISPlay {display_value}"
        self._instrument.write(command)

    def GetChannelDisplay(self, channel):
        """
        Returns the current display setting for the specified channel.
        :param channel: Channel number (1 to # analog channels)
        :return: True if display is on, False if off
        """
        response = self._instrument.query(f":CHANnel{channel}:DISPlay?")
        return True if response.strip() == '1' else False

    def SetDigitalChannelDisplay(self, channel, display_on):
        """
        Turns the digital display on or off for the specified channel.
        This command is only valid for the MSO models.
        :param channel: Channel number (0 to # digital channels - 1)
        :param display_on: True to turn on digital display, False to turn off
        """
        display_value = 'ON' if display_on else 'OFF'
        command = f":DIGital{channel}:DISPlay {display_value}"
        self._instrument.write(command)

    def GetDigitalChannelDisplay(self, channel):
        """
        Returns the current digital display setting for the specified channel.
        This command is only valid for the MSO models.
        :param channel: Channel number (0 to # digital channels - 1)
        :return: True if digital display is on, False if off
        """
        response = self._instrument.query(f":DIGital{channel}:DISPlay?")
        return True if response.strip() == '1' else False