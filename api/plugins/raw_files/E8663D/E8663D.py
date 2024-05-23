from opentap import *
from System import String
import OpenTap

@attribute(OpenTap.Display("E8663D", "A SCPI instrument driver for the Generator E8663D.", "E8663D"))
class GeneratorE8663D(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(GeneratorE8663D, self).__init__()
        self.log = Trace(self)
        self.Name = "E8663D"
    
    def GetIdnString(self):
        a = self.ScpiQuery[String]("*IDN?")
        return a
    
    def reset(self):
        self.normalSCPI("*RST")

    def setFrequency(self, frequency):
        self.normalSCPI(f":FREQ {frequency}")

    def setAmplitude(self, amplitude):
        self.normalSCPI(f":POW:AMPL {amplitude} dBm")

    def setOutputState(self, state):
        state_str = "ON" if state else "OFF"
        self.normalSCPI(f":OUTP {state_str}")

    def opc(self):
        complete = False
        while not complete:
            complete = self.ScpiQuery[bool]("*OPC?")
            time.sleep(0.1)  # Small delay to prevent overloading the communication

    def normalSCPI(self, SCPI):
        self.ScpiCommand(SCPI)
        self.opc()

    def querySCPI(self, format, SCPI):
        result = self.ScpiQuery[format](SCPI)
        self.opc()
        return result