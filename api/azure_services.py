import os
from dotenv import load_dotenv
load_dotenv(override=True)

from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import tiktoken

from code_parser import sentiment_analysis

def callLLM(prompt):
    
    try: 
        client = AzureOpenAI(
            azure_endpoint=os.environ["Forum_GPT4_ENDPOINT"], 
            api_key=os.environ["Forum_GPT4_KEY"],  
            api_version=os.environ["Forum_GPT4_API_VERSION"]
        )

        message_text = [{"role":"system", "content":"You are an AI assistant that helps people Opentap plugins using SCPI commands in Python."}, 
                        {"role": "user", "content": prompt}]

        completion = client.chat.completions.create(
            model="gpt-4-1106-Preview",
            messages = message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        content = completion.choices[0].message.content

        return content
    
    except Exception as e:
        print(f"Error during callLLM: {e}")

def callAISearch(query, TOKEN_LIMIT=1500):

    try:
        service_endpoint=os.environ["AZURE_AI_SEARCH_ENDPOINT"]
        index_name=os.environ["AZURE_AI_INDEX_NAME"]
        key=os.environ["AZURE_AI_SEARCH_API_KEY"]

        search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

        results = search_client.search(search_text=query)

        context = ""
        token_count = 0

        tokenizer = tiktoken.encoding_for_model("gpt-4")

        for result in results:
            content = result['content']
            tokens = tokenizer.encode(content)
            if token_count + len(tokens) <= TOKEN_LIMIT:
                context += content
                token_count += len(tokens)
            else:
                remaining_tokens = TOKEN_LIMIT - token_count
                truncated_content = tokenizer.decode(tokens[:remaining_tokens])
                context += truncated_content
                break
        return context
    
    except Exception as e:
        print(f"Error during AI search: {e}")


def llm_code_check(prompt):
    try:
        client = AzureOpenAI(
            azure_endpoint=os.environ["Forum_GPT4_ENDPOINT"], 
            api_key=os.environ["Forum_GPT4_KEY"],  
            api_version=os.environ["Forum_GPT4_API_VERSION"]
        )    
            
        message_text = [{"role":"system", "content":"You are an AI assistant that helps people verify Opentap plugins."}, 
                        {"role": "user", "content": prompt}]

        completion = client.chat.completions.create(
            model="gpt-4-1106-Preview",
            messages = message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        content = completion.choices[0].message.content
        
        return sentiment_analysis(content)
    
    except Exception as e:
        print(f"Error during llm_code_check: {e}")

   
