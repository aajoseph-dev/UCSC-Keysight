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
        self.normalSCPI(f':DISK:LOAD "{WfmPosPath}", WMEMory1, INT16')
        self.normalSCPI(":WMEMory1:DISPlay ON")
        # self.normalSCPI(f':DISK:DELete "{WfmPosPath}"')
        self.normalSCPI(f':DISK:LOAD "{WfmNegPath}", WMEMory2, INT16')
        self.normalSCPI(":WMEMory2:DISPlay ON")
        # self.normalSCPI(f':DISK:DELete "{WfmNegPath}"')
        self.normalSCPI(":TIMebase:REFerence:PERCent 25")
        self.normalSCPI(":TIMebase:RANGe 1e-05")
        self.normalSCPI(":FUNCtion1:SUBTract WMEMory1, WMEMory2")
        self.normalSCPI(":DISPlay:MAIN OFF, WMEMory1")
        self.normalSCPI(":DISPlay:MAIN OFF, WMEMory2")
        self.normalSCPI(":FUNCtion1:DISPlay ON")

    def eyediagram(self, bitrate):
        self.normalSCPI(':ANALyze:SIGNal:TYPE FUNC1, PAM4')
        self.normalSCPI(':MEASure:STATistics MEAN')
        self.normalSCPI(f':ANALyze:SIGNal:DATarate FUNCtion1, {str(bitrate*1E+09)}')
        self.normalSCPI(":DISPlay:MAIN OFF, FUNCtion1")
        self.normalSCPI(':MTESt:FOLDing On, FUNCtion1')