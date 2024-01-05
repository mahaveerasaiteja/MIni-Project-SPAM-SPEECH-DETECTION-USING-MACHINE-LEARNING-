import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:                # use the default microphone as the audio source
    print("say something")
    audio = r.record(source,duration=7)               # listen for the first phrase and extract it into audio data
    print("time over, thanks")

try:
    text = r.recognize_google(audio)
    print("You said : {}".format(text))
    text = r.recognize_google(audio)
except:
    print('Sorry could not recognize your voice')
