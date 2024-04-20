import requests

def run_test(deviceName, category, commands, interface, progLang, role, useCase):
    payload = {"deviceName" : deviceName,
                "category" : category,  
                "commands" : commands,
                "interface" : interface,
                "progLang" : progLang,
                "role" : role,
                "useCase" : useCase}

    api_url = "http://127.0.0.1:5002/generate_plugin" 
    response = requests.post(api_url, json=payload)

    # Error handling 
    if response.status_code == 200:
        if response.headers.get('Content-Type') == 'application/json':
            result = response.json()
        else:
            try:
                with open(f"/Users/shaun/Desktop/115b/UCSC-Keysight/documents/{deviceName}.zip", 'wb') as f:
                    f.write(response.content)
                print("Downloaded successfully")
            except Exception as e:
                print("error", e)
    else:
        print("Error:", response.status_code, response.text)


test = run_test("EDU36311A", "Power supply", [":DISPLay", ":MEASure"], "USB-B", "python", "As a test engineer, I want to create a plugin in python to test batteries", "generate_plugin")
print(test)
