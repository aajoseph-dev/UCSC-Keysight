from opentap import *
from .E8363BAnalyzer import AnalyzerE8363B

@attribute(Display("Signal Integrity Analysis", "Performs signal integrity analysis on E8363B Analyzer.", "Signal Integrity Analysis"))
class SignalIntegrityAnalysis(TestStep):
    Instrument = property(AnalyzerE8363B, None) \
        .add_attribute(Display("Instrument", "The E8363B Analyzer to use in the step.", "Resources"))

    def __init__(self):
        super(SignalIntegrityAnalysis, self).__init__()
        self.Name = "Signal Integrity Analysis"

    def Run(self):
        super().Run()  # 3.0: Required for debugging to work.

        # Set the type of signal being measured to either 'CLOCK' or 'DATA'
        self.Instrument.normalSCPI(":MEASURE:SINTEGRITY:SIGNAL CLOCK")

        # Query the current signal type setting
        signal_type = self.Instrument.querySCPI(String, ":MEASURE:SINTEGRITY:SIGNAL?")
        self.log.Info(f"Signal Type: {signal_type}")

        # Enable certain bits in the Questionable Integrity Signal Condition Register
        self.Instrument.normalSCPI(":STATus:QUEStionable:INTegrity:SIGNal:ENABle 4")

        # Query the current condition of the signal integrity
        condition_value = self.Instrument.querySCPI(Int32, ":STATus:QUEStionable:INTegrity:SIGNal:CONDition?")
        self.log.Info(f"Signal Integrity Condition Value: {condition_value}")

        # Query the signal integrity event register
        event_value = self.Instrument.querySCPI(Int32, ":STATus:QUEStionable:INTegrity:SIGNal:EVENt?")
        self.log.Info(f"Signal Integrity Event Value: {event_value}")

        if condition_value == 0 and event_value == 0:
            self.UpgradeVerdict(Verdict.Pass)
        else:
            self.UpgradeVerdict(Verdict.Fail)
            self.log.Error("Signal integrity analysis failed.")

# Register the step so it appears in the TAP Editor
TestStepTypes.Add(SignalIntegrityAnalysis)