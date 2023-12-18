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

# similarity checking
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(user_answer, actual_answer):
    if user_answer is None or actual_answer is None:
        return 0.0
    # Tokenization and Lowercasing
    user_tokens = user_answer.lower().split()
    actual_tokens = actual_answer.lower().split()

    # Combine tokens for TF-IDF vectorization
    all_tokens = set(user_tokens + actual_tokens)

    # Vectorize using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_answer, actual_answer])

    # Calculate cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity


@app.route('/check_answers',methods=['POST'])
def check_answers():
    data = request.json
    if not data:
        print("Data is not received correctly")
        return jsonify({"error": "No answers provided"}), 400
    else :
        print("The user's answers are received correctly")
    user_answer = data.get("answers",[]) 
    question_type = request.args.get('type')
    print(question_type)
    score = 0
    # if ques is in MCQ, t/f, one word:
    if question_type in ['MCQ',"TrueFalse","OneWord"]:
        for i in range(len(user_answer)):
            if user_answer[i] in [True,False,None]:
                if user_answer[i]== actualAnswers[i]:
                    score+=1
            elif user_answer[i].lower()== actualAnswers[i].lower():
                score+=1
        return jsonify({"score": score,"questions":questions_asked,"user_answer":user_answer,"actual_answer":actualAnswers})
    else : # else it is one liner:
        for i in range(len(user_answer)):
            similarity = calculate_similarity(user_answer[i], actualAnswers[i])
            # You can set a threshold for similarity; adjust as needed
            if similarity > 0.5:
                score += 1
            elif similarity > 0.2:
                score+=0.5

        return jsonify({"score": score, "questions": questions_asked, "user_answer": user_answer, "actual_answer": actualAnswers})


def get_random_question(question_type=None, difficulty=None):
    print("Fetching questions of type", question_type)
    ques = []
    answer = []
    
    # Set a counter and limit for the loop
    loop_counter = 0
    max_attempts = 100

    while len(ques) < 10 and loop_counter < max_attempts:
        loop_counter += 1

        if question_type and question_type in questions:
            q = random.choice(questions[question_type])
            
            if q['difficulty_category'] == difficulty:
                question_without_answer = {key: value for key, value in q.items() if key != 'answer'}
                if question_without_answer not in ques:
                    ques.append(question_without_answer)
                    ans = {key: value for key, value in q.items() if key == 'answer'}
                    answer.append(ans['answer'])
                    
   
    if ques and answer:
        print("Question fetched successfully..")
    else:
        print("Failed to fetch questions after {} attempts.".format(loop_counter))
        return jsonify({"Error to fetch questions."})
    return [ques, answer]


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
