# importing libraries and modules
import pandas as pd
import random
# dataset integration

df=pd.read_csv("dataset/trueFalse.csv")


# speech engine
import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init('sapi5')   #text to speech (pyttsx3) {sapi5 for win, nsss for mac}
voices = engine.getProperty('voices') # voices attribute created now we can change the voices 
engine.setProperty('voice', voices[0].id) #voices[0]--male voice ,voices[1]--female voice
engine.setProperty('volume',1.0) # can lower voice vol from 0 to 1
engine.setProperty('rate',200) 


# speech engine
import pyttsx3
import speech_recognition as sr


engine=pyttsx3.init('sapi5') #use nsss for mac
voice=engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
engine.setProperty('volume',1.0)
engine.setProperty('rate',150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def record_answer():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold=1
        audio=r.listen(source)

    try:
            print("listening...")
            ans=r.recognize_google(audio,language='en-in')
    except Exception as e:
            return "None"
    return ans

if __name__=="__main__":
    # speak("welcome to the test environment")
    noOfQues=df.shape[0]
    print(noOfQues)
    quesBank=random.sample(range(noOfQues),2)
    print(quesBank)
    for i in quesBank:
        speak(df.iloc[i][0])
        actualAns=df.iloc[i][1]
        ans=record_answer()
        if(ans==str(actualAns).lower()):
            print(ans)
            speak("correct")
        else:
            print(ans)
            speak("incorrect")


