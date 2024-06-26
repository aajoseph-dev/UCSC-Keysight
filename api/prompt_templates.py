#update to focus on plugins not test steps

class PromptTemplates:
    def __init__(self, data):
        self.device_name = data.get("deviceName")
        self.category = data.get("category")
        self.interface = data.get("interface")
        self.prog_lang = data.get("progLang")
        self.role = data.get("role")

    def generate_instrument_prompt(self, context):
        return f"""
        Generate an OpenTAP test instrument declaration in {self.prog_lang} for the following device: {self.device_name} {self.category}
        Instructions:
        - Name your class: {self.device_name}{self.category}
        - Do not import visa or pyvisa
        - Import the following: 
            from opentap import *
            import OpenTap
        - Along with the standard python libraries you have access to these:
            -OpenTap
            -opentap
            -pythonnet==3.0.3
            -numpy==1.26.4
            -debugpy==1.8.1

        Context from Ai search: 
            {context}

        Example code for guidance:
            from opentap import *
            from System import Double, String
            import OpenTap
            import time

            @attribute(OpenTap.Display("Infiniium", "A basic example of a SCPI instrument driver.", "Infiniium"))
            class Scope(OpenTap.ScpiInstrument):
                
                def __init__(self):
                    super(Scope, self).__init__()
                    self.log = Trace(self)
                    self.Name = "Infiniium"
                
                def GetIdnString(self):
                    a = self.ScpiQuery[String]("*IDN?")
                    return a
                
                def reset(self):
                    self.normalSCPI(":SYSTem:PRESet FACTory")

                def Setup(self, WfmPosPath, WfmNegPath ):
                    self.normalSCPI(":CHANnel1:DISPlay OFF")
                    self.normalSCPI(f':DISK:LOAD "{{WfmPosPath}}", WMEMory1, INT16')
                    self.normalSCPI(":WMEMory1:DISPlay ON")
                    # self.normalSCPI(f':DISK:DELete "{{WfmPosPath}}"')
                    self.normalSCPI(f':DISK:LOAD "{{WfmNegPath}}", WMEMory2, INT16')
                    self.normalSCPI(":WMEMory2:DISPlay ON")
                    # self.normalSCPI(f':DISK:DELete "{{WfmNegPath}}"')
                    self.normalSCPI(":TIMebase:REFerence:PERCent 25")
                    self.normalSCPI(":TIMebase:RANGe 1e-05")
                    self.normalSCPI(":FUNCtion1:SUBTract WMEMory1, WMEMory2")
                    self.normalSCPI(":DISPlay:MAIN OFF, WMEMory1")
                    self.normalSCPI(":DISPlay:MAIN OFF, WMEMory2")
                    self.normalSCPI(":FUNCtion1:DISPlay ON")

                def eyediagram(self, bitrate):
                    self.normalSCPI(':ANALyze:SIGNal:TYPE FUNC1, PAM4')
                    self.normalSCPI(':MEASure:STATistics MEAN')
                    self.normalSCPI(f':ANALyze:SIGNal:DATarate FUNCtion1, {{str(bitrate*1E+09)}}')
                    self.normalSCPI(":DISPlay:MAIN OFF, FUNCtion1")
                    self.normalSCPI(':MTESt:FOLDing On, FUNCtion1')
                
                def CTLE(self, symbolRate, dcGain, z1Freq, z2Freq, P1Freq, P2Freq, P3Freq):
                    self.normalSCPI(":LANE1:SOURce Func1")
                    self.normalSCPI(":LANE1:EQUalizer:CTLE:NUMPoles P3Z2")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:DCGain {{dcGain}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:Z1 {{z1Freq}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:Z2 {{z2Freq}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:P1 {{P1Freq}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:P2 {{P2Freq}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:P3 {{P3Freq}}")
                    self.normalSCPI(f":LANE1:EQUalizer:CTLE:RATE{{str(symbolRate*1E+09)}}")
                    self.normalSCPI(':MTESt:FOLDing OFF, FUNCtion1')
                    self.normalSCPI(":LANE1:EQUalizer:CTLE:STATe  ON")
                    self.normalSCPI(":LANE1:STATe ON")
                    self.normalSCPI(':ANALyze:SIGNal:TYPE EQUalized1, PAM4')
                    self.normalSCPI(f':ANALyze:SIGNal:SYMBolrate EQUalized1, {{str(symbolRate*1E+09)}}')

                    self.normalSCPI(":DISPlay:MAIN OFF, EQUalized")
                    
                    self.normalSCPI(':MTESt:FOLDing On, EQUalized')
                    
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


        """

    def generate_steps_prompt(self, command, instrument, context):
        return f"""
        Using the instrument declaration code for {self.device_name} {self.category} please generate a 
        {command} test step.
        
        Instructions:
        - Import the following: 
            from opentap import *
            import OpenTap
        - The code should be in {self.prog_lang}
        - do not add code that already exists in instrument declaration
        - the instrument can be imported using
            from .{self.device_name} import {self.device_name}{self.category}
        - Include functions that utilize the provided SCPI commands.
        - Do not import visa or pyvisa
        - Along with the standard Python libraries you have access to these:
            -OpenTap
            -opentap
            -pythonnet==3.0.3
            -numpy==1.26.4
            -debugpy==1.8.1
        
        Context from AI search: 
            {context}

        Insturment declaration used to connect to the {self.device_name} {self.category}:
            {instrument}

        Example code for guidance:
            import sys
            import opentap
            import clr
            clr.AddReference("System.Collections")
            from System.Collections.Generic import List
            from opentap import *

            import OpenTap 
            import math
            from OpenTap import Log, AvailableValues, EnabledIfAttribute

            ## Import necessary .net APIs
            # These represents themselves as regular Python modules but they actually reflect
            # .NET libraries.
            import System
            from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
            from System.ComponentModel import Browsable # BrowsableAttribute can be used to hide things from the user.
            import System.Xml
            from System.Xml.Serialization import XmlIgnore

            from .Infiniium import Scope
            from .ADS_setup import ADS_setting
            from enum import Enum
            import json

            # Here is how a test step plugin is defined: 

            #Use the Display attribute to define how the test step should be presented to the user.
            @attribute(OpenTap.Display("4. IDN", "A IDN to check the connection.", "InfiniiumAutomation", Order=1))
            #AllowAnyChildAttribute is attribute that allows any child step to attached to this step
            @attribute(OpenTap.AllowAnyChild())
            class BasicFunctionality(TestStep): # Inheriting from opentap.TestStep causes it to be a test step plugin.
                # Add properties (name, value, C# type)
                
                Instrument = property(Scope, None)\
                    .add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))
                    

                def __init__(self):
                    super(BasicFunctionality, self).__init__() # The base class initializer must be invoked.

                
                def Run(self):
                    super().Run() ## 3.0: Required for debugging to work. 
                    
                    
                    idn = self.Instrument.GetIdnString()
                    self.log.Info(idn)
                    
                    # Set verdict
                    self.UpgradeVerdict(OpenTap.Verdict.Pass)
                    

            @attribute(OpenTap.Display("1. Initial Setting", "Inintial setup.", "InfiniiumAutomation", Order=2))
            class InitalSetting(TestStep): # Inheriting from opentap.TestStep causes it to be a test step plugin.
                # Add properties (name, value, C# type)
                
                Instrument = property(Scope, None)\
                    .add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))
                WfmPosPath = property(String, r"C:\EPScan\EDA\AutomationWorkflow\FlexDCA_Probe_example_wrk\data\ADS_Waveform1.csv")\
                    .add_attribute(OpenTap.Display("Positive Waveform", "Positive signal waveform Path", "Parameter", 2))\
                    .add_attribute(OpenTap.FilePath(fileExtension="CSV|*.csv"))    
                WfmNegPath = property(String, r"C:\EPScan\EDA\AutomationWorkflow\FlexDCA_Probe_example_wrk\data\ADS_Waveform2.csv")\
                    .add_attribute(OpenTap.Display("Negative Waveform", "Negative signal waveform Path", "Parameter", 3))\
                    .add_attribute(OpenTap.FilePath(fileExtension="CSV|*.csv"))    

                def __init__(self):
                    super(InitalSetting, self).__init__() # The base class initializer must be invoked.

                
                def Run(self):
                    super().Run() ## 3.0: Required for debugging to work. 
                    
                    self.Instrument.reset()
                    self.Instrument.Setup(self.WfmPosPath, self.WfmNegPath)
                    
                    # Set verdict
                    self.UpgradeVerdict(OpenTap.Verdict.Pass)

             """
    
    def generate_instrument_validation(self, code, context):
        return f"""
        Is the following code an acceptable file to be an test instrument declaration for an OpenTAP plugin. 
        This file is for the {self.device_name} instrument.

        Context from AI search: 
            {context}
                    
        Verify this code:
            {code}
        """

    def generate_step_validation(self, code, command, plugin, context):
        return f"""
        Is the following code an acceptable file to be part of an OpenTAP plugin. 
        This file is a {command} test step for {self.device_name}.

        It should refernce SCPI commands, OpenTAP and utilize this instrument plugin 
        when creating test steps:
            {plugin}

        Context from AI Search: 
            {context}

        Verify this test step code:
            {code}
        """
    
    def failed_insturment(self, code, context, LLM_response, parser_results):
        return f"""

        The OpenTAP plugin instrument declaration for {self.device_name} was not generated properly.
        Please generate a fixed declaration

        Here's the response from another LLM: 
            {LLM_response}

        Here are some errors the code parser found:
            {parser_results}
        
        Context from AI Search: 
            {context}

        Update this code to address these issues:
            {code}
        """
    
    def failed_test_step(self, code, command, context, LLM_response, parser_results):
        return f"""
        The {command} test step for the {self.device_name} was not generated properly.

        Here's the response from another LLM: 
            {LLM_response}

        Here are some errors the code parser found:
            {parser_results}
        
        Context from AI Search: 
            {context}

        Update this code to address these issues:
            {code}
        """
