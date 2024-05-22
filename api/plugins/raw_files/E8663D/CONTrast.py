import opentap
from opentap import *
from System import String
import clr
clr.AddReference("System")
clr.AddReference("OpenTap")
import OpenTap
from OpenTap import DisplayAttribute, Instrument

import visa
import time

@attribute(DisplayAttribute, "E8663D Signal Generator", "SCPI Interface to control display settings on an E8663D PSG Signal Generator.", "Python Example")
class E8663DSignalGenerator(Instrument):
    def __init__(self):
        super().__init__() # The base class initializer must be invoked.
        self.Name = "E8663D Signal Generator"
        self._resource_manager = visa.ResourceManager()
        self._instrument = None
    
    def Open(self):
        super().Open()
        # Assuming the instrument VISA address is 'GPIB0::10::INSTR'. Replace with the actual address of your instrument.
        self._instrument = self._resource_manager.open_resource('GPIB0::10::INSTR')

    def Close(self):
        if self._instrument is not None:
            self._instrument.close()
        super().Close()

    def set_contrast(self, contrast_value):
        if 0 <= contrast_value <= 1:
            self._instrument.write(f":DISP:CONT {contrast_value:.2f}")
        else:
            raise ValueError("Contrast value must be between 0 and 1")

    def get_contrast(self):
        return float(self._instrument.query(":DISP:CONT?"))

    def set_display_inverse(self, inverse_on):
        value = "ON" if inverse_on else "OFF"
        self._instrument.write(f":DISP:INV {value}")

    def get_display_inverse(self):
        response = self._instrument.query(":DISP:INV?")
        return True if response.strip() == "1" else False

    def set_remote_display_update(self, remote_on):
        value = "ON" if remote_on else "OFF"
        self._instrument.write(f":DISP:REM {value}")

    def get_remote_display_update(self):
        response = self._instrument.query(":DISP:REM?")
        return True if response.strip() == "1" else False

# Example usage:
if __name__ == "__main__":
    sg = E8663DSignalGenerator()
    try:
        sg.Open()
        sg.set_contrast(0.45)  # Set contrast to 0.45
        print("Current contrast:", sg.get_contrast())
        
        sg.set_display_inverse(True)  # Enable inverse video mode
        print("Inverse video mode:", "ON" if sg.get_display_inverse() else "OFF")
        
        sg.set_remote_display_update(False)  # Disable remote display update
        print("Remote display update:", "ON" if sg.get_remote_display_update() else "OFF")
    finally:
        sg.Close()