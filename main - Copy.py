#---------------------------importing libraries and modules---------------------------
import pandas as pd
import random
from fuzzywuzzy import fuzz
import pyttsx3
import speech_recognition as sr
from difficulty_level_in_ques import mcq_data,oword_data,oline_data,tf_data


# -------------------here the code for speech starts---------------------------
# ----------above is the dataframe---------------------------------------------

engine=pyttsx3.init('sapi5') #use nsss for mac
voice=engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
engine.setProperty('volume',1.0)
engine.setProperty('pitch',100)
engine.setProperty('rate',150)

# speech
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()
# listening
def record_answer():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold=0.8
        r.energy_threshold=100
        audio=r.listen(source)

    try:
            print("listening")
            ans=r.recognize_google(audio,language='en-GB')
            print(ans)
    except Exception as e:
            return "None"
    return ans
# true false
def trueFalse(score_acquired,total_questions):
    df=tf_data
    speak("Please speak true or false only")
    noOfQues=df.shape[0]
    quesBank=random.sample(range(noOfQues),2)
    total_questions+=len(quesBank)
    print(quesBank)
    valid_ans=['true','false']
    for i in quesBank:
        speak(df.iloc[i][0])
        actualAns=df.iloc[i][1]
        ans=record_answer()
        while(ans not in valid_ans):
            speak("please repeat in true false only")
            ans=record_answer()
        if(ans==str(actualAns).lower()):
            speak("correct")
            score_acquired+=1
        elif(ans !=None):
            speak("incorrect")
        else:
            speak("No answer received")
    return (score_acquired,total_questions)
# one word
def oneWord(score_acquired,total_questions):
    speak("Please answer in one word")
    df=oword_data
    noOfQues=df.shape[0]
    quesBank=random.sample(range(noOfQues),2)
    total_questions+=len(quesBank)
    print(quesBank)
    for i in quesBank:
        speak(df.iloc[i][0])
        actualAns=df.iloc[i][1]
        ans=record_answer()
        if(ans==str(actualAns).lower()):
            speak("correct")
            score_acquired+=1
        elif(ans !=None):
            speak("incorrect")
        else:
            speak("No answer received")
    
    return (score_acquired,total_questions)
# mcq
def mcq(score_acquired,total_questions):
    # df=pd.read_csv("./dataset/PreprocessedDataSetMCQ.csv")
    df=mcq_data
    noOfQues=df.shape[0]
    quesBank=random.sample(range(noOfQues),2)
    total_questions+=len(quesBank)
    valid_ans=['option a','option b','option c','option d']
    speak("Please only speak the option in terms of option A option B option C option D")
    for i in quesBank:
        # question
        speak(df.iloc[i][0])
        speak("Option A")
        speak(df.iloc[i][1])
        speak("Option B")
        speak(df.iloc[i][2])
        speak("Option C")
        speak(df.iloc[i][3])
        speak("Option D")
        speak(df.iloc[i][4])
        # actual answer
        actualAns=df.iloc[i][5]
        ans=record_answer()
        while(ans.lower() not in valid_ans):
            speak("Please speak only the option")
            ans=record_answer()
        if(ans[-1].lower()==str(actualAns).lower()):
            print(ans[-1].lower())
            speak("correct")
            score_acquired+=1
        else:
            print(ans[-1].lower())
            speak("incorrect")
            speak("The correct answer is :")
            speak(df.iloc[i][5])
            speak("the Explanation of this is :")
            speak(df.iloc[i][6])
    return(score_acquired,total_questions)

def check_similarity(user_answer, correct_answer):
    similarity_ratio = fuzz.ratio(user_answer.lower(), correct_answer.lower())
    return similarity_ratio

def oneLiner(score_acquired,total_questions):
    df=oline_data
    noOfQues=df.shape[0]
    quesBank=random.sample(range(noOfQues),2)
    total_questions+=len(quesBank)
    print(quesBank)

    for i in quesBank:
            speak(df.iloc[i][0])
            actualAns=df.iloc[i][1]
            ans=record_answer()
            similarity_ratio=check_similarity(user_answer=ans,correct_answer=actualAns)

            if similarity_ratio>=70:
                 print("Correct! Your answer matches the stored answer.")
                 score_acquired+=1
            else:
                  print("Answer can be frames as :",df.iloc[i][1])
    
    return (score_acquired,total_questions)

# __main__
def answer_question():
    # keeping record of the correct answer
    score_acquired=0;
    total_questions=0;
    speak("welcome to the test environment")
    # asking MCQ
    (mcq_score,questions_asked)=mcq(score_acquired=0,total_questions=0)
    score_acquired+=mcq_score
    total_questions+=questions_asked
    print("Score in MCQ",mcq_score)
    # asking True False
    (true_false_score,questions_asked)=trueFalse(score_acquired=0,total_questions=0)
    score_acquired+=true_false_score
    total_questions+=questions_asked
    print("Score in True/False",mcq_score)

    # asking One word
    (oneWord_score,questions_asked)=oneWord(score_acquired=0,total_questions=0)
    score_acquired+=oneWord_score
    total_questions+=questions_asked
    print("Score in one word",oneWord_score)
    # asking one liner
    (oneLiner_score,questions_asked)=oneLiner(score_acquired=0,total_questions=0)
    score_acquired+=oneLiner_score
    total_questions+=questions_asked
    print("Score in one Liners",oneLiner_score)
    print(score_acquired,total_questions)

