from opentap import *
from System import Double, String
import OpenTap
import time

@attribute(OpenTap.Display("Generator asdf", "A SCPI instrument driver for the Generator asdf.", "Generator asdf"))
class GeneratorAsdf(OpenTap.ScpiInstrument):

    def __init__(self):
        super(GeneratorAsdf, self).__init__()
        self.log = Trace(self)
        self.Name = "Generator asdf"

    def GetIdnString(self):
        a = self.ScpiQuery[String]("*IDN?")
        return a

    def Reset(self):
        self.normalSCPI("*RST")

    def SetFrequency(self, frequency):
        # Assuming the SCPI command for setting frequency is :FREQ
        self.normalSCPI(f":FREQ {frequency}")

    def SetAmplitude(self, amplitude):
        # Assuming the SCPI command for setting amplitude is :VOLT
        self.normalSCPI(f":VOLT {amplitude}")

    def SetOutput(self, state):
        # Assuming the SCPI command for turning on/off the output is :OUTP
        on_off = "ON" if state else "OFF"
        self.normalSCPI(f":OUTP {on_off}")

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