Based on the instructions provided, the goal is to create a Python class that inherits from OpenTap's TestStep to enable the display test of the EDU36311A Power Supply. The class will use the SCPI command to perform the display test. Since the EDU36311A Power Supply has a colorful WVGA display, and assuming that the SCPI command for testing the display is `DISP:TEST ON` (this command may vary depending on the actual device's programming guide), the code might look something like this:

```python
from opentap import *
from .EDU36311APowerSupply import EDU36311APowerSupply

@attribute(Display("Enable Display Test", "Enables the display test on the EDU36311A Power Supply", "EDU36311A Power Supply"))
class EnableDisplayTestStep(TestStep):
    Instrument = property(EDU36311APowerSupply, None).add_attribute(Display("Instrument", "The power supply to use in the step.", "Resources"))

    def __init__(self):
        super(EnableDisplayTestStep, self).__init__() # The base class initializer must be invoked.

    def Run(self):
        super().Run() ## Required for debugging to work.
        if self.Instrument is None:
            self.log.Error("Instrument is not set.")
            self.UpgradeVerdict(Verdict.Fail)
            return
        
        # Enable display test
        self.Instrument.normalSCPI("DISP:TEST ON")
        
        # Optional: Check if the display test was enabled successfully
        # This would require knowing the SCPI query command to check the display test status
        
        # Assuming the display test was successfully enabled
        self.log.Info("Display test enabled.")
        
        # Set verdict to Pass if everything went well
        self.UpgradeVerdict(Verdict.Pass)

# Register the EnableDisplayTestStep
OpenTap.TapPlan.Current.AddStep(EnableDisplayTestStep)
```

Please note that `DISP:TEST ON` is a placeholder SCPI command. You need to replace this command with the actual command from the EDU36311A's SCPI programming guide to enable the display test.

Also, the above code assumes that the `EDU36311APowerSupply` class has been defined correctly and contains the `normalSCPI` method that sends SCPI commands to the instrument and waits for the operation to complete. If the actual SCPI command to enable the display test is different, or if additional steps are required to verify the success of the operation, you will need to adjust the code accordingly.