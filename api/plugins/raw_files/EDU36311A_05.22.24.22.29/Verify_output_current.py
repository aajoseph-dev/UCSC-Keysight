from opentap import *
from .EDU36311APowerSupply import EDU36311A

@attribute(Display("Verify Output Current", "Test step to verify the output current of the EDU36311A Power Supply.", "Power Supply Verification"))
class VerifyOutputCurrent(TestStep):
    Instrument = property(EDU36311A, None) \
        .add_attribute(Display("Instrument", "The instrument to use in the step.", "Resources"))
    
    ExpectedCurrent = property(float, 0.0) \
        .add_attribute(Display("Expected Current (A)", "Expected current value in amperes to verify against the measured value.", "Test Parameters"))
    
    Tolerance = property(float, 0.05) \
        .add_attribute(Display("Tolerance (A)", "Acceptable tolerance in amperes for the current measurement.", "Test Parameters"))
    
    Channel = property(int, 1) \
        .add_attribute(Display("Channel", "The output channel to measure the current from.", "Test Parameters"))
    
    def __init__(self):
        super(VerifyOutputCurrent, self).__init__()
    
    def Run(self):
        super().Run()
        
        # Measure the current from the specified channel
        measured_current = self.Instrument.MeasureCurrent(self.Channel)
        
        # Check if the measured current is within the expected range
        lower_bound = self.ExpectedCurrent - self.Tolerance
        upper_bound = self.ExpectedCurrent + self.Tolerance
        
        if lower_bound <= measured_current <= upper_bound:
            self.UpgradeVerdict(Verdict.Pass)
            self.log.Info(f"Measured current {measured_current}A is within the expected range ({lower_bound}A to {upper_bound}A).")
        else:
            self.UpgradeVerdict(Verdict.Fail)
            self.log.Error(f"Measured current {measured_current}A is outside the expected range ({lower_bound}A to {upper_bound}A).")