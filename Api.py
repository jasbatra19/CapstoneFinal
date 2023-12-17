from flask import Flask, jsonify, request
import random
from flask_cors import CORS
from difficulty_level_in_ques import mcq_data, oline_data, oword_data, tf_data
import pandas as pd

app = Flask(__name__)
CORS(app)  

def handle_nan(value):
    return '' if pd.isna(value) else value

questions = {
    'MCQ': mcq_data.applymap(handle_nan).to_dict(orient='records'),
    'TrueFalse': tf_data.applymap(handle_nan).to_dict(orient='records'),
    'OneWord': oword_data.applymap(handle_nan).to_dict(orient='records'),
    'OneLiner': oline_data.applymap(handle_nan).to_dict(orient='records')
}
actualAnswers=[]
questions_asked=[]
@app.route('/check_answers',methods=['POST'])
def check_answers():
    data = request.json
    user_answer = data.get("answers",[]) 
    print(actualAnswers)
    score = 0
    for i in range(len(user_answer)):
        if user_answer[i] in [True,False,None]:
            if user_answer[i]== actualAnswers[i]:
                score+=1
        elif user_answer[i].lower()== actualAnswers[i].lower():
            score+=1
    return jsonify({"score": score,"questions":questions_asked,"user_answer":user_answer,"actual_answer":actualAnswers})


def get_random_question(question_type=None,difficulty=None):
    ques=[]
    answer=[]
    while len(ques)<10:
        if question_type and question_type in questions:
            q=random.choice(questions[question_type])
            if q['difficulty_category']==difficulty:
                question_without_answer = {key: value for key, value in q.items() if key != 'answer'}
                if question_without_answer not in ques :
                    ques.append(question_without_answer)
                    ans={key:value for key, value in q.items() if key=='answer'}
                    answer.append(ans['answer'])

    return [ques,answer]

@app.route('/random_question', methods=['GET'])
def random_question():
    question_type = request.args.get('type')
    difficulty = request.args.get('difficulty')
    [question,actualans] = get_random_question(question_type,difficulty)
    global actualAnswers, questions_asked
    actualAnswers=actualans
    questions_asked=question
    return jsonify(question)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
