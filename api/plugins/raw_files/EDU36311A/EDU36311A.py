The following Python code can be used to implement the Startup function for the EDU36311A Generators using SCPI commands:

```python
# Set up the VISA resource manager
import visa
rm = visa.ResourceManager()

# Connect to the power supply
power_supply = rm.open_resource("USB0::0x0957::0x1B11::MY51141234::INSTR")

# Reset the power supply to its default settings
power_supply.write("*RST")

# Turn on the output
power_supply.write("OUTPut ON")
``` 

Note: This code assumes that the power supply is connected to the computer via USB and that the VISA resource manager has been properly installed. The specific USB address and device ID may need to be adjusted based on the user's setup.