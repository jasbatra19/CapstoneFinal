import requests
from bs4 import BeautifulSoup
import pandas as pd

def extractData():
    # response = requests.get(url)
    with open('response.html', 'r') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    data = []
    questions = soup.find_all('span', class_='ques')

    for index, question in enumerate(questions):
        ques_text = question.text.strip()
        answer_texts = []

        next_element = question.next_sibling
        while next_element and not (next_element.name == 'span' and index > 0):
            if next_element.name == 'p':
                answer_texts.append(next_element.text.strip())
        #     elif next_element.name in ['ul', 'ol']:
        #         bullet_points = next_element.find_all('li')
        #         answer_text = ''
        #         for bullet_point in bullet_points:
        #             bullet_text = bullet_point.text.strip()
        #             answer_text += f"- {bullet_text}\n"
        #         answer_texts.append(answer_text.strip())
            next_element = next_element.next_sibling

        data.append({'questions': ques_text, 'answers': answer_texts})

    return data

url = "https://www.javatpoint.com/operating-system-interview-questions"
data = extractData()

df = pd.DataFrame(data)  # Convert the list of dictionaries to a DataFrame
df.to_csv('questionAnswer.csv', index=False)  # Save the DataFrame to a CSV file
print(df)
print("Data saved to data.csv")