from gtts import gTTS

transformToMP3 = input("What Do You Want Transformed to an MP3? ")

def create_mp3(result):
    language = 'en'
    mp3 = gTTS(text = f"{ result }", lang=language)
    mp3.save('Text_To_Speech.mp3')

create_mp3(transformToMP3)