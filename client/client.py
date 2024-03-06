import requests

api_url = "http://127.0.0.1:5000/generate_plugin"  # Update with your API endpoint
question = "Give me a full list of front panel controls for E364xA power supply"  # Update with your question

# Define the payload
payload = {"question": question}

# Make the POST request
response = requests.post(api_url, json=payload)

# Check the response
if response.status_code == 200:
    result = response.json()
    generated_plugin = result.get("generated_plugin", "")
    print("Generated Plugin:", generated_plugin)
else:
    print("Error:", response.status_code, response.text)
