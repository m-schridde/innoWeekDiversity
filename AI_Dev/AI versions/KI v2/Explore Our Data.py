
from explore_data import * 
from load_dataset import *

data_path = os.path.join(os.path.dirname(__file__), "Data")
test1, test2 = load_dataset(data_path)
median = get_num_words_per_sample(test1[0])
numberOfSamples = len(test1[0])
print("Median" +str(median))
print("S/W: "+str(numberOfSamples/median))
plot_frequency_distribution_of_ngrams(test1[0])
plot_sample_length_distribution(test1[0])
print(get_num_classes(test1[1]))
plot_class_distribution(test1[1])