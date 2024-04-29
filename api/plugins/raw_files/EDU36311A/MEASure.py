
import visa

class EDU36311APowerSupply:
    def __init__(self, resource_name):
        # Assuming that PyVISA is being used to communicate with instruments
        self.rm = visa.ResourceManager()
        self.instr = self.rm.open_resource(resource_name)
        
    def configure_wlan_dsss(self):
        # Configure the VSA for WLAN DSSS measurement
        self.instr.write(":CONFigure:W11B")
    
    def configure_wlan_dsss_default(self):
        # Set the WLAN DSSS measurement to default configuration
        self.instr.write(":CONFigure:W11B:NDEFault")
    
    def initiate_wlan_dsss(self):
        # Initiate the WLAN DSSS measurement
        self.instr.write(":INITiate:W11B")
        
    def fetch_wlan_dsss_results(self, trace_number=1):
        # Fetch results from the WLAN DSSS measurement
        results = self.instr.query(f":FETCh:W11B{trace_number}?")
        return results.strip().split(',')
    
    def measure_wlan_dsss_results(self, trace_number=1):
        # Measure results from the WLAN DSSS measurement
        results = self.instr.query(f":MEASure:W11B{trace_number}?")
        return results.strip().split(',')
    
    def read_wlan_dsss_results(self, trace_number=1):
        # Read results from the WLAN DSSS measurement
        results = self.instr.query(f":READ:W11B{trace_number}?")
        return results.strip().split(',')
    
    def close(self):
        # Close the connection to the instrument
        self.instr.close()

# Example usage:
if __name__ == "__main__":
    # Replace 'USB0::0x2A8D::0x1301::MY12345678::0::INSTR' with the actual address of your device
    resource_name = 'USB0::0x2A8D::0x1301::MY12345678::0::INSTR'
    power_supply = EDU36311APowerSupply(resource_name)
    
    try:
        power_supply.configure_wlan_dsss()
        power_supply.initiate_wlan_dsss()
        results = power_supply.fetch_wlan_dsss_results()
        print("WLAN DSSS Results:", results)
    finally:
        power_supply.close()
