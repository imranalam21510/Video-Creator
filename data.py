from allosaurus.app import read_recognizer
import tts.sapi


def textToWav(text):
    voice = tts.sapi.Sapi()
    voice.create_recording('welcome.wav', text)


data = input("Enter your Script here:- ")
text = ' '.join(word for word in data.split() if word[0]!='[')
textToWav(text)
# load your model
model = read_recognizer()

# run inference -> æ l u s ɔ ɹ s
abc = model.recognize('./welcome.wav',timestamp=True)
print(abc)
print("completed")