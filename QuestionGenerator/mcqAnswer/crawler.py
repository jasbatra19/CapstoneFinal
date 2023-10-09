from bs4 import BeautifulSoup
import pandas as pd
import re

def extractData():
   
    with open('response.html', 'r') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    

    data = []
    questions = soup.find_all('span', class_='ques')

    for index, question in enumerate(questions):
        ques_text = question.text.strip()
        answer_texts=[]
        answer = []
        explanation = []
        option1=[]
        option2=[]
        option3=[]
        option4=[]
        

        next_element = question.next_sibling
        while next_element and not (next_element.name == 'span' and index > 0):
            if next_element.name == 'p':
                answer_texts.append(next_element.text.strip())

            next_element = next_element.next_sibling

        data.append({'questions': ques_text, 'answers': answer_texts})

    return data


data = extractData()

df = pd.DataFrame(data)  
df.to_csv('questionAnswer.csv', index=False) 
print(df)
print("Data saved to data.csv")