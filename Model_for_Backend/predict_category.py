import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle
import numpy as np
from Model_for_Backend.data_preparation import TOP_K


NGRAM_RANGE = (1, 2)
TOKEN_MODE = 'word'
CATEGORY_LIST = ["Culture and Identity", "Differently-Abled People", "Gender Intelligence", "Family and Career"]
THRESHHOLD_OFFSET_FACTOR=1.2

path = os.path.join(os.path.dirname(__file__), "TAG_mlp_model.h5")
my_model = tf.keras.models.load_model(path)

kwargs = {
        'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
        'dtype': 'int32',
        'strip_accents': 'unicode',
        'decode_error': 'replace',
        'analyzer': TOKEN_MODE,  # Split text into word tokens.
}

vectorizer = TfidfVectorizer(**kwargs, max_features = TOP_K)
feature_list = pickle.load(open("Model_for_Backend/feature.pkl", "rb"))
vectorizer.fit(feature_list)

def is_covid_problem(problem):
    problem = problem.lower()
    corona_words = ['corona', 'pandemic', 'quarantine', 'epidemic', 'virus', 'covid']
    if any(corona_word in problem for corona_word in corona_words):
        return True

def predict_category(problem):
    list_x = [problem]
    x = vectorizer.transform(list_x) 
    x = x.toarray()
    result = my_model.predict(x)
    result_list = list(result[0])
    number_of_tags = len(CATEGORY_LIST)
    threshhold = (1/number_of_tags) * THRESHHOLD_OFFSET_FACTOR
    tags = []
    for tag in result_list:
        if tag > threshhold:
            tags.append(CATEGORY_LIST[result_list.index(tag)])
    if is_covid_problem(problem):
        tags.append("Covid-19")
    return tags

# while True:
#     input_x = input("What bothers you?: ")
#     print(predict_category(input_x))
