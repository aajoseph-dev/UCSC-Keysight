
import visa

class PowerSupplyDisplay:
    def __init__(self, resource_name):
        # Establish connection to the instrument
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)

    def enable_display(self, enable=True):
        """
        Enable or disable the display of the power supply.
        :param enable: True to enable the display, False to disable it.
        """
        state = 'ON' if enable else 'OFF'
        self.instrument.write(f':DISPlay:ENABle {state}')

    def query_display_enabled(self):
        """
        Query the current status of the display (enabled or disabled).
        :return: True if the display is enabled, False if it is disabled.
        """
        response = self.instrument.query(':DISPlay:ENABle?')
        return True if response.strip() == '1' else False

    def set_display_layout(self, layout):
        """
        Set the display layout of the power supply.
        :param layout: The desired layout mode ('V-V', 'I-I', or 'V-I').
        """
        valid_layouts = ['V-V', 'I-I', 'V-I']
        if layout not in valid_layouts:
            raise ValueError(f"Invalid layout mode. Choose from {valid_layouts}")
        self.instrument.write(f':DISPlay:LAYout {layout}')

    def close(self):
        # Close the connection to the instrument
        self.instrument.close()

# Example Usage:
if __name__ == "__main__":
    # Replace with the actual resource name of your instrument
    resource_name = 'USB0::0x2A8D::0x1202::MY1234567::INSTR'
    ps_display = PowerSupplyDisplay(resource_name)
    
    try:
        # Enable the display
        ps_display.enable_display(True)
        # Query the display status
        is_enabled = ps_display.query_display_enabled()
        print(f"Display Enabled: {is_enabled}")
        # Set the display layout to V-I
        ps_display.set_display_layout('V-I')
    finally:
        ps_display.close()
