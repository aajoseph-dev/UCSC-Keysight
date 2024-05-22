import opentap
from opentap import *
import visa
import numpy as np

@attribute(DisplayAttribute, "E8363B Network Analyzer", "Plugin for controlling E8363B Network Analyzer using SCPI commands.", "Network Analyzers")
class E8363BNetworkAnalyzer(Instrument):
    def __init__(self):
        super().__init__()  # Initialize base class
        self._rm = visa.ResourceManager()
        self._instrument = None
        self.Name = "E8363B Network Analyzer"
        self.Address = "GPIB0::16::INSTR"
        
    def Open(self):
        super().Open()
        self._instrument = self._rm.open_resource(self.Address)
        self._instrument.write("*CLS")  # Clear the instrument
        
    def Close(self):
        if self._instrument is not None:
            self._instrument.close()
        super().Close()
        
    def _write_scpi(self, command):
        if self._instrument is not None:
            self._instrument.write(command)
            
    def _query_scpi(self, command):
        if self._instrument is not None:
            return self._instrument.query(command).strip()
        return None
        
    @method(None, [Double])
    def SetFrequencyDeviation(self, frequency):
        cmd = f":WGEN:MODulation:FM:DEViation {frequency}"
        self._write_scpi(cmd)
        
    @method(Double)
    def QueryFrequencyDeviation(self):
        response = self._query_scpi(":WGEN:MODulation:FM:DEViation?")
        return float(response) if response else None
        
    @method(None, [Double])
    def SetCenterFrequencyOffset(self, frequency_offset):
        cmd = f"FREQ:CENT:OFFS {frequency_offset}"
        self._write_scpi(cmd)
        
    @method(Double)
    def QueryCenterFrequencyOffset(self):
        response = self._query_scpi("FREQ:CENT:OFFS?")
        return float(response) if response else None
        
    @method(None, [Double])
    def SetCenterFrequency(self, frequency):
        cmd = f"FREQ:CENT {frequency}"
        self._write_scpi(cmd)
        
    @method(Double)
    def QueryCenterFrequency(self):
        response = self._query_scpi("FREQ:CENT?")
        return float(response) if response else None
        
    # You can add more methods here for other SCPI commands as needed.

# Register the instrument plugin
Instrument.Add(E8363BNetworkAnalyzer)

# You can also define additional classes for other subsets of SCPI commands if needed.