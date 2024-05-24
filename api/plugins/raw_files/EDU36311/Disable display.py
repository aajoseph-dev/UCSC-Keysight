import sys
import opentap
import clr
import time
clr.AddReference("System.Collections")
from System.Collections.Generic import List
from opentap import *

import OpenTap
from OpenTap import Log, AvailableValues, EnabledIfAttribute

import System
from System import Array, Double, Byte, Int32, String, Boolean

@attribute(OpenTap.Display("EDU36311 Power Supply", "SCPI Instrument Driver for EDU36311 Power Supply", "EDU36311"))
class PowerSupplyEDU36311(OpenTap.ScpiInstrument):
    
    def __init__(self):
        super(PowerSupplyEDU36311, self).__init__()
        self.Name = "EDU36311"

    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")

    def reset(self):
        self.ScpiCommand("*RST")

    # ...other methods for voltage setting and querying...

    def enableDisplay(self):
        self.ScpiCommand("DISP:ENAB ON")

    def disableDisplay(self):
        self.ScpiCommand("DISP:ENAB OFF")

    def queryDisplayEnabled(self):
        return self.ScpiQuery[Boolean]("DISP:ENAB?")

# Example usage of the plugin
@attribute(OpenTap.Display("Disable Display", "Disable the display of EDU36311 Power Supply", "Power Supply Control"))
class DisableDisplayTestStep(OpenTap.TestStep):
    Instrument = property(PowerSupplyEDU36311, None) \
        .add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))

    def __init__(self):
        super(DisableDisplayTestStep, self).__init__() # The base class initializer must be invoked.

    def Run(self):
        super().Run() # Required for debugging to work.
        self.Instrument.disableDisplay()
        if not self.Instrument.queryDisplayEnabled():
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.UpgradeVerdict(OpenTap.Verdict.Fail)