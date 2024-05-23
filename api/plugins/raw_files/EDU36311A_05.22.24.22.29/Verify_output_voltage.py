from opentap import *
from .EDU36311APowerSupply import EDU36311A

@attribute(Display("Verify Output Voltage", "Test step to verify the output voltage of the Keysight EDU36311A Power Supply.", "Power Supply Verification"))
class VerifyOutputVoltage(TestStep):
    Instrument = property(EDU36311A, None).add_attribute(Display("Instrument", "The power supply instrument to use in the step.", "Resources"))
    ExpectedVoltage = property(float, 0).add_attribute(Display("Expected Voltage", "The expected output voltage to verify.", "Parameters", 1))
    VoltageTolerance = property(float, 0.1).add_attribute(Display("Voltage Tolerance", "The tolerance for the output voltage verification.", "Parameters", 2))
    Channel = property(int, 1).add_attribute(Display("Channel", "The channel to verify the output voltage on.", "Parameters", 3))
    
    def __init__(self):
        super(VerifyOutputVoltage, self).__init__()
    
    def Run(self):
        super().Run()
        measured_voltage = self.Instrument.MeasureVoltage(self.Channel)
        lower_limit = self.ExpectedVoltage - self.VoltageTolerance
        upper_limit = self.ExpectedVoltage + self.VoltageTolerance
        
        if lower_limit <= measured_voltage <= upper_limit:
            self.UpgradeVerdict(Verdict.Pass)
            self.log.Info(f"Channel {self.Channel} output voltage is within tolerance: {measured_voltage} V")
        else:
            self.UpgradeVerdict(Verdict.Fail)
            self.log.Error(f"Channel {self.Channel} output voltage is out of tolerance: {measured_voltage} V (expected: {self.ExpectedVoltage} V ± {self.VoltageTolerance} V)")

# Register the step so that OpenTAP can recognize it
TestStep.Register(VerifyOutputVoltage())