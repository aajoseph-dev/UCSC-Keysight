from dotenv import load_dotenv
import os

from openai import AzureOpenAI
from nltk.sentiment.vader import SentimentIntensityAnalyzer


from promptTemplates import *
from app import *


def llm_code_check(prompt): 
    load_dotenv()

    sid = SentimentIntensityAnalyzer()

    client = AzureOpenAI(
            azure_endpoint = "https://opentap-forum-openai.openai.azure.com/", 
            api_key=os.getenv("Forum-GPT4_KEY1"),  
            api_version="2024-02-15-preview"
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
    scores = sid.polarity_scores(content)

    if scores['compound'] >= 0.25: 
        return {"Sentiment" : "Positive", "Response" : content}
    elif scores['compound'] <= -0.25: 
        return {"Sentiment" : "Negative", "Response" : content}
    else:
        return {"Sentiment" : "Neutral", "Response" : content}
