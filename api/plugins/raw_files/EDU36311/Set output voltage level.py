from opentap import *
from System import Double, String
import OpenTap

@attribute(OpenTap.Display("EDU36311 Power Supply", "SCPI Instrument Driver for EDU36311 Power Supply", "EDU36311"))
class PowerSupplyEDU36311(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(PowerSupplyEDU36311, self).__init__()
        self.Name = "EDU36311"

    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")

    def reset(self):
        self.ScpiCommand("*RST")

    def setVoltage(self, voltage, immediate=True):
        if immediate:
            self.ScpiCommand(f"VOLT {voltage}")
        else:
            self.ScpiCommand(f"VOLT:TRIG {voltage}")

    def queryVoltage(self, immediate=True):
        if immediate:
            return self.ScpiQuery[Double]("VOLT?")
        else:
            return self.ScpiQuery[Double]("VOLT:TRIG?")

    def setVoltageMode(self, mode):
        assert mode in ["FIXed", "STEP"], "Invalid mode"
        self.ScpiCommand(f"VOLT:MODE {mode}")

    def queryVoltageMode(self):
        return self.ScpiQuery[String]("VOLT:MODE?")

    def setVoltageProtection(self, level):
        self.ScpiCommand(f"VOLT:PROT {level}")

    def queryVoltageProtection(self):
        return self.ScpiQuery[Double]("VOLT:PROT?")

    def setPostType(self, post_type):
        assert post_type in ["TRIGgered", "STARt", "STOP", "BASE"], "Invalid post type"
        self.ScpiCommand(f"VOLT:POST:TYPE {post_type}")

    def queryPostType(self):
        return self.ScpiQuery[String]("VOLT:POST:TYPE?")

    def outputOn(self):
        self.ScpiCommand("OUTP ON")

    def outputOff(self):
        self.ScpiCommand("OUTP OFF")

    def opc(self):
        complete = self.ScpiQuery[Double]("*OPC?")
        while complete != 1:
            time.sleep(0.1)
            complete = self.ScpiQuery[Double]("*OPC?")