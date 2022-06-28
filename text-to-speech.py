from gtts import gTTS
import os

file = open("assets/text-to-speech.txt", mode="r", encoding="utf-8").read()

speech = gTTS(text=file, lang="vi", slow=False)
speech.save("assets/voice.mp3")
os.system("assets/voice.mp3")
