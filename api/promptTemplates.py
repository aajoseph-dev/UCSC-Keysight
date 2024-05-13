#update to focus on plugins not test steps

class PromptTemplates:
    def __init__(self, data, context):
        self.device_name = data.get("deviceName")
        self.category = data.get("category")
        self.interface = data.get("interface")
        self.prog_lang = data.get("progLang")
        self.role = data.get("role")
        self.context = context

    def generate_plugin_prompt(self, command):
        print(f"""Generate an OpenTAP plugin class for a subset of scpi commands for the given device.
        Context:
        - Device Name: {self.device_name}
        - Category: {self.category}
        - Command: {command}
        - Interface: {self.interface}
        - Programming Language: {self.prog_lang}
        - Role: {self.role}
        """)

        return f"""Generate an OpenTAP plugin class for a subset of scpi commands for the given device.
        Context:
        - Device Name: {self.device_name}
        - Category: {self.category}
        - Command: {command}
        - Interface: {self.interface}
        - Programming Language: {self.prog_lang}
        - Role: {self.role}
        - Documentation: {self.context}
        
        Instructions:
        - In {self.prog_lang} generate code for this subset of SCPI commands.
        - Include functions that utilize the provided SCPI commands.
        - Follow best practices for the specified programming language and role.
        - Along with the standard python libraries you have access to these:
            -OpenTap
            -opentap
            -pythonnet==3.0.3
            -PyVISA==1.14.1
            -visa==2.21.0
            -numpy==1.26.4
            -debugpy==1.8.1

        Example code for guidance:

            Simulated Power Analyzer example.

            This power analyzer simulation simulates charging and discharging a battery and measuring the voltage meanwhile.

            The instrument plugin created by this example is accessible from a .NET API by referencing the built example directly.
            From a .NET point of view, the assembly is called Python.PluginExample.dll and the instrument is named Python.PluginExample.PowerAnalyzer.
            import opentap
            from opentap import *
            from System import Double, Random #Import types to reference for generic methods
            from System.Diagnostics import Stopwatch
            import OpenTap
            from OpenTap import DisplayAttribute

            @attribute(DisplayAttribute, "Power Analyzer", "Simulated power analyzer instrument used for charge/discharge demo steps written in python.", "Python Example")
            class PowerAnalyzer(Instrument):
                CellSizeFactor = property(Double, 0.005)\
                    .add_attribute(DisplayAttribute, "Cell Size Factor", "A larger cell size will result in faster charging and discharging.")
                def __init__(self):
                    super().__init__() # The base class initializer must be invoked.
                    self._voltage = 1.0
                    self._cellVoltage = 2.7
                    self._current = 10
                    self._currentLimit = 0.0
                    self._sw = None
                    self.Name = "PyPowerAnalyzer"

                def Open(self):
                    super().Open()
                    self._voltage = 0
                    self._cellVoltage = 2.7

                def Close(self):
                    if self._sw != None:
                        self._sw.Stop()
                    super().Close()
                @method(Double)
                def MeasureCurrent(self):
                    self.UpdateCurrentAndVoltage()
                    return self._current

                @method(Double)
                def MeasureVoltage(self):
                    self.UpdateCurrentAndVoltage()
                    return self._cellVoltage
                @method(None, [Double, Double])
                def Setup(self, voltage, current):
                    self._voltage = voltage
                    self._currentLimit = current
                    self._current = current
                @method()
                def EnableOutput(self):
                    if self._sw == None or self._sw.IsRunning == False:
                        self._sw = Stopwatch.StartNew()
                @method()
                def DisableOutput(self):
                    if self._sw != None:
                        self._sw.Stop()

                def UpdateCurrentAndVoltage(self):
                    if self._sw == None or self._sw.IsRunning == False:
                        return

                    # Generates a somewhat random curve that gradually approaches the limit.
                    self._current = self._currentLimit * ((self._voltage - self._cellVoltage) * 2) + Random().NextDouble() * self._currentLimit / 50.0;

                    if self._current >= self._currentLimit:
                        self._current = self._currentLimit;
                    elif self._current < 0 - self._currentLimit:
                        self._current = 0 - self._currentLimit;

                    self._cellVoltage += self.CellSizeFactor * self._current * self._sw.Elapsed.TotalSeconds * 10;
                    self._sw.Restart();
                    """
