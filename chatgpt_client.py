import os
import openai
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

question = input("What is your question for chatGPT? ")

def ask_question():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot" },
            {"role": "user", "content": f"{ question }" },
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    print(f"We asked chatGPT { question } - here is their response: ")
    print(result)
    return(result)

def create_mp3(result):
    language = 'en'
    mp3 = gTTS(text = f"{ result }", lang=language)
    mp3.save(f'{ question }.mp3')

answer = ask_question()
create_mp3(answer)