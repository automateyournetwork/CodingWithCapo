import os
import json
import openai
import requests
from gtts import gTTS
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
webexToken = os.getenv("WEBEX_TOKEN")
webexRoomId = os.getenv("WEBEX_ROOMID")

question = input("What is your question for chatGPT? ")

def ask_question():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot" },
            {"role": "user", "content": f"{ question }" },
        ]
    )

    answer = ''
    for choice in response.choices:
        answer += choice.message.content

    print(f"We asked chatGPT { question } - here is their response: ")
    print(answer)
    return(answer)

def create_mp3(answer):
    language = 'en'
    mp3 = gTTS(text = f"{ answer }", lang=language)
    mp3.save(f'{ question }.mp3')

def send_chat_to_webex(answer):
    url = "https://webexapis.com/v1/messages"

    payload = json.dumps({
        "roomId": f" { webexRoomId }",
        "text": f"We asked chatGPT { question }"
    }
    )

    headers = {
        "Authorization": f"Bearer { webexToken }",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"The Webex API call had a response code of: { response }")

    payload = json.dumps({
        "roomId": f" { webexRoomId }",
        "text": f"Here was chatGPT's answer:\n{ answer } "
    }
    )

    headers = {
        "Authorization": f"Bearer { webexToken }",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"The Webex API call had a response code of: { response }")\

def send_mp3_to_webex():
    url = "https://webexapis.com/v1/messages"
       
    message_with_mp3 = MultipartEncoder(
        {
        "roomId": f"{ webexRoomId }",
        "text": f"We asked chatGPT { question }",
        "files": (
            f"{ question }.mp3", open(f"{ question }.mp3", 'rb'),
            'audio/mp3')
        }
    )

    response = requests.post(url,data=message_with_mp3,headers={"Authorization": f"Bearer { webexToken }","Content-Type": f"{ message_with_mp3.content_type }"})
    print(response)

answer = ask_question()
create_mp3(answer)
if webexToken:
    send_chat_to_webex(answer)
    send_mp3_to_webex()