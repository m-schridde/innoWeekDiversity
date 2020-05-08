import os
import random
import numpy as np

def load_dataset(data_path, seed=123):
    # Load the training data
    train_texts = []
    train_labels = []
    categories = ['Autism', 'Ethnicity', 'Gender Equality', 'LGBTQ+', 'Religion']
    for category in categories:
        train_path = os.path.join(data_path, 'Training', category)
        for fname in sorted(os.listdir(train_path)):
            if fname.endswith('.txt'):
                with open(os.path.join(train_path, fname), encoding="utf-8") as f:
                    train_texts.append(f.read())
                train_labels.append(categories.index(category))

    # Load the validation data.
    test_texts = []
    test_labels = []
    for category in categories:
        test_path = os.path.join(data_path, 'Test', category)
        for fname in sorted(os.listdir(test_path)):
            if fname.endswith('.txt'):
                with open(os.path.join(test_path, fname), encoding="utf-8") as f:
                    test_texts.append(f.read())
                test_labels.append(categories.index(category))

    # Shuffle the training data and labels.
    random.seed(seed)
    random.shuffle(train_texts)
    random.seed(seed)
    random.shuffle(train_labels)

    return ((train_texts, np.array(train_labels)),
            (test_texts, np.array(test_labels)))
