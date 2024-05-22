from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("EDU36311A USB", "A SCPI instrument driver for EDU36311A USB device.", "EDU36311A USB"))
class EDU36311A_USB(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311A_USB, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A USB"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def Reset(self):
        self.ScpiCommand("*RST")
        self.opc()

    # Add other methods to control and interface with the device as needed.
    # The following are placeholder methods and should be replaced with actual functionality.
    
    def SetVoltage(self, voltage):
        # Assume the device has a command to set voltage like: "VOLT <value>"
        self.ScpiCommand(f"VOLT {voltage}")
        self.opc()

    def SetCurrent(self, current):
        # Assume the device has a command to set current like: "CURR <value>"
        self.ScpiCommand(f"CURR {current}")
        self.opc()

    def MeasureVoltage(self):
        # Assume the device has a query to measure voltage like: "MEAS:VOLT?"
        measured_voltage = self.ScpiQuery[String]("MEAS:VOLT?")
        return measured_voltage

    def MeasureCurrent(self):
        # Assume the device has a query to measure current like: "MEAS:CURR?"
        measured_current = self.ScpiQuery[String]("MEAS:CURR?")
        return measured_current

    def opc(self):
        # Operation complete query to ensure the previous command has finished.
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[Double]('*OPC?')
    
    def normalSCPI(self, SCPI):
        # Send a normal SCPI command and wait for it to complete.
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        # Send a SCPI query, get the result and wait for it to complete.
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result