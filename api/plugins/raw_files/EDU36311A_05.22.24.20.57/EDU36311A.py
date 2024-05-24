from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("EDU36311A Power Supply", "A basic example of a SCPI instrument driver for the EDU36311A Power Supply.", "Power Supplies"))
class EDU36311APowerSupply(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(EDU36311APowerSupply, self).__init__()
        self.log = Trace(self)
        self.Name = "EDU36311A Power Supply"
    
    def GetIdnString(self):
        idn_string = self.ScpiQuery[String]("*IDN?")
        return idn_string
    
    def Reset(self):
        self.normalSCPI("*RST")
    
    def ConfigureOutput(self, channel, voltage, current):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI(f"VOLT {voltage}")
        self.normalSCPI(f"CURR {current}")
    
    def OutputOn(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP ON")
    
    def OutputOff(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        self.normalSCPI("OUTP OFF")
    
    def MeasureVoltage(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        voltage = self.querySCPI(Double, "MEAS:VOLT?")
        return voltage
    
    def MeasureCurrent(self, channel):
        self.normalSCPI(f"INST:NSEL {channel}")
        current = self.querySCPI(Double, "MEAS:CURR?")
        return current
    
    def opc(self):
        complete = self.ScpiQuery[Double]('*OPC?')
        while complete != 1:
            complete = self.ScpiQuery[Double]('*OPC?')
    
    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()
    
    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result

# Remember to register the instrument so OpenTAP can recognize it
OpenTap.TapSettings.CurrentSettings.InstrumentSettings.Add(EDU36311APowerSupply())