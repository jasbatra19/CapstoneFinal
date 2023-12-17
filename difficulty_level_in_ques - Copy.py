import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer


# Load the CSV files for different question types
mcq_data = pd.read_csv("dataset/PreprocessedDataSetMCQ.csv")
oline_data = pd.read_csv("dataset/PreprocessedDataSetOneLiners.csv")
tf_data=pd.read_csv("dataset/trueFalse.csv")
oword_data=pd.read_csv("dataset/oneWord.csv")

# Preprocess the text data
def preprocess_text(text):
        if isinstance(text, str):
            # check for null
            words = nltk.word_tokenize(text)
            words = [word.lower() for word in words]
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words]
            stemmer = PorterStemmer()
            lemmatizer = WordNetLemmatizer()
            stemmed_words = [stemmer.stem(word) for word in words]
            lemmatized_words = [lemmatizer.lemmatize(word) for word in stemmed_words]
            processed_text = ' '.join(lemmatized_words)
            return processed_text
        else:
            return '' 
    

# calculate difficulty
def categorize_difficulty(score):
    if score <= 10:
        return "easy"
    elif score <= 20:
        return "medium"
    else:
        return "hard"

def scale_difficulty(dataframe):
    difficulty_scores = []

    for question in dataframe["question"]:
        words = nltk.word_tokenize(question)
        question_tags = nltk.pos_tag(words)
        
        difficulty_score = 0
        for _, tag in question_tags:
            if tag in ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "JJ", "JJR", "JJS"]:
                difficulty_score += 1
            elif tag == "RB" or tag == "RBR" or tag == "RBS":
                difficulty_score += 0.5
        difficulty_scores.append(difficulty_score)

    # Scale the difficulty scores to a 0-30 range
    scaled_difficulty_scores = [(score / max(difficulty_scores)) * 30 for score in difficulty_scores]

    # Assign the scaled difficulty scores to the questions.
    dataframe["difficulty_level"] = scaled_difficulty_scores

    # Categorize the difficulty levels
    dataframe["difficulty_category"] = dataframe["difficulty_level"].apply(categorize_difficulty)

    return dataframe



for dataframe in [mcq_data,oline_data,tf_data,oword_data]:
    dataframe=scale_difficulty(dataframe)


# Preprocess MCQ
cleaned_mcq_data = mcq_data.copy()
columns_to_preprocess = ['question', 'A', 'B', 'C', 'D', 'answer', 'explanation']
for column in columns_to_preprocess:
    cleaned_mcq_data[column] = cleaned_mcq_data[column].apply(preprocess_text)

# Preprocess One Liners data
cleaned_oline_data = oline_data.copy()
cleaned_oline_data['question'] = cleaned_oline_data['question'].apply(preprocess_text)
cleaned_oline_data['answer'] = cleaned_oline_data['answer'].apply(preprocess_text)

#  Preprocess True/False data
cleaned_tf_data = tf_data.copy()
cleaned_tf_data['question'] = cleaned_tf_data['question'].apply(preprocess_text)
cleaned_tf_data['answer'] = cleaned_tf_data['answer'].apply(preprocess_text)

#  Preprocess One Word data
cleaned_oword_data = oword_data.copy()
cleaned_oword_data['question'] = cleaned_oword_data['question'].apply(preprocess_text)
cleaned_oword_data['answer'] = cleaned_oword_data['answer'].apply(preprocess_text)

# Calculate similar questions and remove similar questions
def vectorization(data):
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(data)
    cosine_similarities = cosine_similarity(question_vectors, question_vectors)
    similarity_threshold = 0.8
    questions_to_remove = []
    for i in range(len(cosine_similarities)):
        for j in range(i + 1, len(cosine_similarities)):
            if cosine_similarities[i][j] > similarity_threshold:
                avg_similarity_i = sum(cosine_similarities[i]) / len(cosine_similarities[i])
                avg_similarity_j = sum(cosine_similarities[j]) / len(cosine_similarities[j])
                
                if avg_similarity_i > avg_similarity_j:
                    questions_to_remove.append(j)
                else:
                    questions_to_remove.append(i)

    return questions_to_remove

# List of original DataFrames and their corresponding cleaned versions
data_frames = [
    (mcq_data, cleaned_mcq_data),
    (oline_data, cleaned_oline_data),
    (oword_data, cleaned_oword_data),
    (tf_data, cleaned_tf_data)
]

# Iterate over the original DataFrames and their cleaned versions
for original_dataframe, cleaned_dataframe in data_frames:
    questions_to_remove = vectorization(cleaned_dataframe['question'])
    original_dataframe.drop(original_dataframe.index[questions_to_remove], inplace=True)


print(mcq_data)
print(oline_data)
print(oword_data)
print(tf_data)