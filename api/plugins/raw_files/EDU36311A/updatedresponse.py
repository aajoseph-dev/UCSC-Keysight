import clr

class EDU36311ADriver:
    def __init__(self, connection):
        self.connection = connection
        
    def display_enable(self,state):
        """
        Controls the display enable mode global.
        
        Type: remote command only
        
        Syntax:
           :DISPlay:ENABle {ON|OFF|1|0}
           :DISPlay:ENABle?"""
        if state == 'ON' or state == 'OFF' or state == '1' or state == '0':
            self.connection.send(':DISPlay:ENABle {}'.format(state))
            return True
        else:
            return False

def turn_display_off(self):
    """
    Turns off the display for an EDU36311A power supply
    """
    self.connection.display_enable('OFF')


def turn_display_on(self):
    """
    Turns on the display for an EDU36311A power supply
    """
    self.connection.display_enable('ON')


import argparse

# Import your EDU36311ADriver instance here

if __name__ == "__main__":
    
    # Parse command line arguments here
    
    # Instantiate EDU36311ADriver here
    
    # Use driver instance here    
    connection.display_enable('OFF')
    print("Display turned off")
    
    connection.display_enable('ON')
    print("Display turned on")


import sys                     # Required for system calls
import io                                                                                       # Required for translation to bytes
import visa                     # Required for SCPI commands
from time import sleep          # Required for sleep commands

class EDU36311A:
        def __init__(self):
                rm = visa.ResourceManager()
                resources = rm.list_resources()
                for resource in resources:
                        if '82357B' in resource:
                                self.inst = rm.open_resource(resource)
                                self.inst.timeout = 30000

        def connect(self):
                return self.inst.query('*IDN?')

        def disconnect(self):
                self.inst.close()

        def cmd(self):
                self.inst.open()

        def query(self, cmd: str):
                return self.inst.query(cmd)

        def write(self, cmd: str):
                self.inst.write(cmd)

        def read_raw(self) -> bytes:
                return self.inst.read_raw()

        def set_output_voltage(self, value: int):
                self.inst.write(f"VOLT {value}")

        def read_output_voltage(self):
                        return self.inst.query("VOLT?")

        def set_output_current(self, value: int):
                self.inst.write(f"CURR {value}")

        def read_output_current(self):
                return self.inst.query("CURR?")

        def set_volt_and_curr_levels(self, voltage: int, current: int):
                self.write(f"APPL {voltage}, {current}")

        def turn_on():
                self.write("OUTPUT ON")

        def turn_off():
                self.write("OUTPUT OFF")

# --- UNIT TESTS (place at bottom of file) --- #

def EDU36311A_test():
        ps = EDU36311A()
        assert ps.connect()), 'Initialization test failed.'
        assert ps.disconnect(), 'Disconnection test failed.'

        test_voltage = 3.3
        test_current = 0.400
        ps.cmd()
        ps.set_volt_and_curr_levels(test_voltage, test_current)
        assert ps.read_output_voltage() == test_voltage, 'Voltage level test failed.'
        assert ps.read_output_current() == test_current , 'Current level test failed.'

# Test the function by invoking it directly
if __name__ == "__main__":
   EDU36311A_test()
<|im_sep|>