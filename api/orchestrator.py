import os
import sys
from openai import AzureOpenAI
from dotenv import load_dotenv


if __name__ == "__main__":

    load_dotenv()

    client = AzureOpenAI(
    azure_endpoint = "https://opentappluginai.openai.azure.com/", 
    api_key=os.getenv("OPENAI_KEY1"),  
    api_version="2024-02-15-preview"
    )

    device = sys.argv[1]
    catergory = sys.argv[2]
    message_text = [{"role":"system","content":"generate a C++ outline for a opentap plugin for the {} {}".format(device, catergory)}]
    print(message_text)
    
    ''''
    completion = client.chat.completions.create(
    model="OpenTap-Plugin-LLM", 
    messages = message_text,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    print(completion.choices[0].message.content)

    ''''
