import random
from flask import Flask, render_template, redirect
import speech_recognition as sr
import pyttsx3
from main import mcq_data

app = Flask(__name__)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please speak your question.")
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio)
        speak("You said: " + question)
        return question
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your question.")
        return None
    except sr.RequestError as e:
        speak("There was an error with the speech recognition service.")
        return None





# ---------------Fill Ups-----------------------------------------------------
#----------------OneLines-----------------------------------------------------
#----------------One Word-----------------------------------------------------
# ---------------Multiple Choice Questions -----------------------------------
score_acquired_mcq = 0
total_mcq_asked = 0
questions_limit = 5

@app.route('/questionMCQ')
def question_asked():
    global score_acquired_mcq
    global total_mcq_asked
    if total_mcq_asked >= questions_limit:
        return redirect('/result')
    df = mcq_data
    no_of_questions = df.shape[0]
    if total_mcq_asked < questions_limit:
        ques_bank = random.sample(range(no_of_questions), questions_limit)
        for i in ques_bank:
            ques = df.iloc[i][0]
            option1 = df.iloc[i][1]
            option2 = df.iloc[i][2]
            option3 = df.iloc[i][3]
            option4 = df.iloc[i][4]
            answer = df.iloc[i][5]
            explanation = df.iloc[i][6]
            difficulty = df.iloc[i][7]

        total_mcq_asked += 1

        return render_template('index.html', ques=ques, options=[option1, option2, option3, option4],
                               answer=answer, explanation=explanation, difficulty=difficulty,
                               score_acquired_mcq=score_acquired_mcq, total_mcq_asked=total_mcq_asked)

@app.route('/result')
def result_mcq():
    global score_acquired_mcq
    global total_mcq_asked
    return render_template('result.html', score_acquired_mcq=score_acquired_mcq, total_mcq_asked=total_mcq_asked)

@app.route('/reset')
def reset_mcq():
    global total_mcq_asked
    global score_acquired_mcq
    total_mcq_asked = 0
    score_acquired_mcq = 0
    return redirect('/questionMCQ')

if __name__ == '__main__':
    app.run(debug=True)
