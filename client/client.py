import requests
#This allows you to send requests to the python api
#I used python for this as it would require the use of visual studio and a windows computer 
#could be run from our macs for testing

 #api_url specific the request
api_url = "http://127.0.0.1:5000/generate_py" 

#this question is passed to the chatbot, modify to change request
question = "Give me a full list of front panel controls for E364xA power supply"  

test_string = {"name": "helloworld.py", 
               "data": "print('hello world')"}

# Since the api takes in a json request the question is formatted to accordingly 
payload = {"question": question}

# The response is sent to the specificed url, in our case its the generate plugin function
response = requests.post(api_url, json=test_string)

#checks if a valid response was returned, printing the output if valid otherwise printing error code
if response.status_code == 200:
    if response.headers.get('Content-Type') == 'application/json':
        result = response.json()
    else:
        try:
            with open('download_file.py', 'wb') as f:
                f.write(response.content)
            print("downloaded succesfully")
        except Exception as e:
            print("error", e)
else:
    print("Error:", response.status_code, response.text)