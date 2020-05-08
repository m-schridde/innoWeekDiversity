import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle
import numpy as np
from Model_for_Backend_New.data_preparation import TOP_K


NGRAM_RANGE = (1, 2)
TOKEN_MODE = 'word'
CATEGORY_LIST = ["Culture and Identity", "Differently-Abled People", "Gender Intelligence", "Family and Career"]
SUB_CATEGORY_LIST = ['Autism', 'Ethnicity', 'Gender Equality', 'LGBTQ+', 'Religion']
THRESHHOLD_OFFSET_FACTOR = 1.2
SUB_THRESHHOLD_OFFSET_FACTOR = 2

path = os.path.join(os.path.dirname(__file__), "TAG_mlp_model.h5")
my_model = tf.keras.models.load_model(path)

sub_path = os.path.join(os.path.dirname(__file__), "sub_TAG_mlp_model.h5")
sub_my_model = tf.keras.models.load_model(sub_path)

kwargs = {
        'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
        'dtype': 'int32',
        'strip_accents': 'unicode',
        'decode_error': 'replace',
        'analyzer': TOKEN_MODE,  # Split text into word tokens.
}

vectorizer = TfidfVectorizer(**kwargs, max_features = TOP_K)
feature_list = pickle.load(open("Model_for_Backend_New/feature.pkl", "rb"))
vectorizer.fit(feature_list)

sub_vectorizer = TfidfVectorizer(**kwargs, max_features = TOP_K)
sub_feature_list = pickle.load(open("Model_for_Backend_New/sub_feature.pkl", "rb"))
sub_vectorizer.fit(sub_feature_list)

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

    sub_x = sub_vectorizer.transform(list_x)
    sub_x = sub_x.toarray()
    sub_result = sub_my_model.predict(sub_x)
    sub_result_list = list(sub_result[0])
    print(sub_result_list)
    sub_number_of_tag = len(SUB_CATEGORY_LIST)
    sub_threshhold = (1/sub_number_of_tag) * SUB_THRESHHOLD_OFFSET_FACTOR
    for tag in sub_result_list:
        if tag > sub_threshhold:
            tags.append(SUB_CATEGORY_LIST[sub_result_list.index(tag)])
    return tags

# while True:
#     input_x = input("What bothers you?: ")
#     print(predict_category(input_x))
