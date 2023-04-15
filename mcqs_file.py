import pandas as pd
import pyttsx3
import speech_recognition as sr

# Read the CSV file
data = pd.read_csv('G:/questions.csv')

data['option1']=data['option1'].astype(str)
data['option2']=data['option2'].astype(str)
data['option3']=data['option3'].astype(str)
data['option4']=data['option4'].astype(str)

# Extract the questions and options into separate lists
questions = data['question'].tolist()
options = data[['option1', 'option2', 'option3', 'option4']].values.tolist()

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')

# # Initialize the speech recognizer
recognizer = sr.Recognizer()

# # Loop through the questions and options
for i, question in enumerate(questions):
    # Speak the question using the text-to-speech engine
    engine.say(question)
    engine.runAndWait()
    
    # Convert the options to a string
    option_str = ', '.join(options[i])
    
    # Speak the options using the text-to-speech engine
    engine.say('The options are ' + option_str)
    engine.runAndWait()
    
    # Listen for the user's answer using the speech recognizer
    with sr.Microphone() as source:
        print('Say your answer...')
        recognizer.pause_threshold=0.8
        recognizer.energy_threshold=100
        audio=recognizer.listen(source)
        
    try:
        # Convert the user's speech to text
        print("listening....")
        user_answer = recognizer.recognize_google(audio,language='en-US')
        print('You said:', user_answer)
        
        answer=user_answer[user_answer.index(" ")+1]
        # answer=user_answer[len(user_answer)-1]#In this we are getting wrong answer as sometimes the system is picking up option D as option Di.

        if answer.lower()==data['correct'][i]:
            engine.say('Correct') 
        else:
            engine.say('Incorrect. The correct answer is ' + data['correct'][i])
        
        # Speak the response using the text-to-speech engine
        engine.runAndWait()
        
    except sr.UnknownValueError:
        print('Could not understand your answer')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
