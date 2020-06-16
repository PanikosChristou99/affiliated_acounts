import nltk
import os
import csv

import pandas as pd

training_data_location = os.path.join('D:/affiliated_acounts', 'Data', 'stance-data',
                                      'data-all-annotations', 'trainingdata-all-annotations.txt')
file1 = open(training_data_location, 'r')
lines = file1.readlines()[1:]
# print(lines)
lines_tokenized = [line.split() for line in lines]
# print(lines_tokenized)
data = [line[3:-4] for line in lines_tokenized if line[1] == 'Hillary' and line[2] == 'Clinton']
print(data)
df = pd.DataFrame(data)
df.to_csv("./final_data.csv", sep=' ', index=False)


# now i have the data i need

def find_nnps_from_data(data):
    tagged_data = [nltk.pos_tag(tweet_text) for tweet_text in data]
    # print(tagged_data)
    nnp_list_of_lists = [[i for i in tagged_text if i[1] == 'NNP'] for tagged_text in tagged_data]  # find only NNP
    nnp_list_of_lists = [nnp_list for nnp_list in nnp_list_of_lists if nnp_list != []]  # remove empty ones
    print(nnp_list_of_lists)
    with open('final_tweets_from_training_that_target_=_hillary_and_ony_contain_NNP_tag.csv', 'w',
              newline='') as result_file_tags:
        df = pd.DataFrame(nnp_list_of_lists)
        df.to_csv("./final_data_tagged.csv", sep=' ', index=False)
