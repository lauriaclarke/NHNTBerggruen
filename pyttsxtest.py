#import pyttsx3
#engine = pyttsx3.init('sapi5')
#voices = engine.getProperty('voices')
#for voice in voices:
#    print(voice, voice.id)
#    engine.setProperty('voice', voice.id)
#    engine.say("Hello World!")
#    engine.runAndWait()
#    engine.stop()


import pyttsx3
engine = pyttsx3.init()
volume = engine.getProperty('volume')
engine.setProperty('volume', volume-0.5)
print(engine.getProperty('volume'))
engine.runAndWait()
print(engine.getProperty('volume'))

voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
