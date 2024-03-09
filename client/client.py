import requests
#This allows you to send requests to the python api
#I used python for this as it would require the use of visual studio and a windows computer 
#could be run from our macs for testing

#api_url specific the request
api_url = "http://127.0.0.1:5000/generate_plugin" 

#this question is passed to the chatbot, modify to change request
question = "Give me a full list of front panel controls for E364xA power supply"  

xml_string = {'name' : "download_file.py", 
              'py_file' : '/Users/shaun/Desktop/115b/UCSC-Keysight/api/download_file.py',
              'file_path' : '/Users/shaun/Desktop/115b/UCSC-Keysight/test/E364xA'}


test_string = {"name": "asdfasf.py", 
               "data": "print('hello world')\nprint('hello world2')"}

# Since the api takes in a json request the question is formatted to accordingly 
payload = {"plugin_name" : "E364xA",
            "question": question}

# # The response is sent to the specificed url, in our case its the generate plugin function
# file_name = requests.post(api_url, json=payload)
# api_url = f"http://127.0.0.1:5000/download_file/{file_name}"
# response = requests.post(api_url)

response = requests.post(api_url, json=payload)

#checks if a valid response was returned, printing the output if valid otherwise printing error code
if response.status_code == 200:
    if response.headers.get('Content-Type') == 'application/json':
        result = response.json()
    else:
        try:
            with open('files.zip', 'wb') as f:
                f.write(response.content)
            print("Downloaded successfully")
        except Exception as e:
            print("error", e)
else:
    print("Error:", response.status_code, response.text)
