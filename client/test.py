import requests

def run_test(deviceName, category, commands, interface, progLang, role, useCase):
    # payload = {"deviceName" : deviceName,
    #             "category" : category,  
    #             "commands" : commands,
    #             "interface" : interface,
    #             "progLang" : progLang,
    #             "role" : role,
    #             "useCase" : useCase}
    payload = {'deviceName': 'EDU36311', 'category': 'Power Supply', 'commands': ['Set output voltage level', 'Disable display'], 'interface': 'USB (Universal Serial Bus)', 'progLang': 'python', 'role': 'developer'}

    api_url = "http://127.0.0.1:5003/generate_plugin" 
    response = requests.post(api_url, json=payload)

    # Error handling
    if response.status_code == 200:
        if response.headers.get('Content-Type') == 'application/json':
            result = response.json()
            print(result)  # Handle JSON response if needed
        else:
            # Save the zip file locally
            try:
                with open(f"{deviceName}.zip", 'wb') as f:
                    f.write(response.content)
                print("Downloaded successfully")
            except Exception as e:
                print("Error:", e)
    else:
        print("Error:", response.status_code, response.text) 


test = run_test("EDU36311A", "Power supply", [":DISPLay"], "USB-B", "python", "As a test engineer, I want to create a plugin in python to test batteries", "generate_plugin")
# test = run_test("E8363B", "Network Analyzer", [":PRESet", ":FREQuency"], "", "python", "As a test engineer, I want to create a plugin in python to analyze networks", "generate_plugin")

# PSG Signal Generator
test = run_test("E8663D", "PSG Signal Generator", [":CONTrast", ":DATA"], "", "python", "As a test engineer, I want to create a plugin in python to generate signals", "generate_plugin")

# Digital Multimeters (DMM), 34470A
# test = run_test("34470A", "Digital Multimeter", [":CALCulate:SCALe:DB:REFerence", ":CALibration:STRing"], "", "python", "As a test engineer, I want to create a plugin in python to interface with a Digital Multimeter", "generate_plugin")
# test = run_test("34470A", "Digital Multimeter", [":CALCulate:SCALe:DB:REFerence"], "", "python", "As a test engineer, I want to create a plugin in python to interface with a Digital Multimeter", "generate_plugin")

print(test)
