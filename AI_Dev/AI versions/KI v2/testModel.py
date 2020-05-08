import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pickle
from data_preparation import TOP_K

# Vectorization parameters
# Range (inclusive) of n-gram sizes for tokenizing text.
NGRAM_RANGE = (1, 2)

# Whether text should be split into word or character n-grams.
# One of 'word', 'char'.
TOKEN_MODE = 'word'


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
feature_list = pickle.load(open("feature.pkl", "rb"))
vectorizer.fit(feature_list)
while True:
    input_x = input("What bothers you?: ")
    list_x = [input_x]
    x = vectorizer.transform(list_x) 
    x = x.toarray()
    result = my_model.predict(x)
    print("Cultural Identity: "+str(result[0][0]) + "\nDifferently-Abled People: "+str(result[0][1])+"\nGender Intelligence: "+str(result[0][2]) + "\nFamily and Career: " +str(result[0][3]))        