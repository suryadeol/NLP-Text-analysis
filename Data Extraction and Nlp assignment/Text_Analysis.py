#!/usr/bin/env python
# coding: utf-8

# # Importing neccessary libraries

# In[32]:


import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
#nltk.download('punkt')
from nltk.corpus import cmudict
#nltk.download('cmudict')
from nltk.corpus import stopwords
import string
#nltk.download('stopwords')
from nltk.tokenize import SyllableTokenizer
import re
from sklearn.preprocessing import MinMaxScaler
from numpy import *
import warnings as w

w.filterwarnings('ignore')


# # 1. SENTIMENT ANALYSIS :
# # 1.1 Extracting stop words from given folder to ignore them during analysis time

# In[33]:


#extracting stop words from given folder to ignore them during analysis time

import os

# Define the folder path where stop word files are located
folder_path = 'StopWords/StopWords'

# Create an empty set to store the stop words
stop_words = set()

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a text file
    if filename.endswith('.txt'):
        # Open the file for reading
        with open(os.path.join(folder_path, filename), 'r') as f:
            # Read the contents of the file into a string
            text = f.read()
            # Tokenize the string into individual words
            words = text.split()
            # Add the words to the set of stop words
            stop_words.update(words)

# Print the set of stop words
print(stop_words)


# #  1.2 Creating a dictionary of Positive and Negative words

# In[34]:


positive_words_path = 'MasterDictionary/MasterDictionary/positive-words.txt'
negative_words_path = 'MasterDictionary/MasterDictionary/negative-words.txt'

# Create empty dictionaries for positive and negative words
positive_words = {}
negative_words = {}

def make_pn_dictonary():
    # Open the positive words file for reading
    with open(positive_words_path, 'r') as f:
        # Loop through each line in the file
        for line in f:
            # Strip any whitespace and convert to lowercase
            word = line.strip().lower()
            # Check if the word is not in the stop words set
            if word not in stop_words:
                # Add the word to the positive words dictionary with a score of 1
                positive_words[word] = 1

    # Open the negative words file for reading
    with open(negative_words_path, 'r') as f:
        # Loop through each line in the file
        for line in f:
            # Strip any whitespace and convert to lowercase
            word = line.strip().lower()
            # Check if the word is not in the stop words set
            if word not in stop_words:
                # Add the word to the negative words dictionary with a score of -1
                negative_words[word] = -1



# # Calling functions for making dictonary of positive and negative words

# In[35]:


make_pn_dictonary()
# Print the positive and negative word dictionaries
print("Positive words:", positive_words)
print("Negative words:", negative_words)


# #  1.3 Extracting Derived variables
# 

# In[36]:


#tokenize with nltk module
def text_token(file_name):
    # read the text file
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()

    # tokenize the text
    tokens = word_tokenize(text)

    # print the list of tokens
    #print(tokens)
    return tokens,text


# In[37]:


#Caluculaing positive score
positive_score = 0
def posit_score(tokens):
    #since i am using direct values because at the time of making positive dictionary i made positive key word with value '1'
    global positive_score 
    for token in tokens:
        if token.lower() in positive_words:
            positive_score += positive_words[token.lower()]
    print("positive_score",positive_score)
    return positive_score
    
#Caluculaing negative score 
negative_score = 0
def negat_score(tokens):
    #since i am using direct values because at the time of making negative dictionary i made negative key word with value '-1'
    #using -1 to multiply with negative score at time to make it positive value
    global negative_score 
    for token in tokens:
        if token.lower() in negative_words:
            negative_score += negative_words[token.lower()]
    print("Negative score",negative_score * (-1))
    return (negative_score*(-1))
    
#caluculating polarity score
def polar_score():
    polarity_score = (positive_score-negative_score)/((positive_score+negative_score)+0.000001)
    #print("polarity score without normalization",polarity_score)
    #applying normalization over here to get in desired range (-1 to +1) {using min-max-scaling}
    polarity_score = ((polarity_score + 300) / 600) * 2 - 1
    #normalized_score = ((polarity_score - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
    #min_value=-300 max_value=+300
    #new_min=-1 new_max=+1
    print("Polarity_score",polarity_score)
    return polarity_score
    
#caluculating subjective_score
def subject_score(tokens):
    subjective_score= (positive_score+negative_score)/((len(tokens)-len(stop_words))+0.000001)
    #applying normalization to make subjective score in range between 0 to 1 {using min_max_scaling}
    #normalized subjective score is given by: ((subjective_score-min_value)/(max_value-min_value))*(new_max-new_min)+new_min
    min_value=-80
    max_value=80
    new_max=1
    new_min=0
    subjective_score=((subjective_score-min_value)/(max_value-min_value))*(new_max-new_min)+new_min
    
    print("subjective_score",subjective_score)
    return subjective_score


# # 2.Analysis of Readability

# In[38]:


def analysis_readability(text,tokens):

    
    # tokenize the text into sentences
    sentences = sent_tokenize(text)

    # count the number of sentences
    global num_sentences
    num_sentences = len(sentences)

    # print the result
    #print("Number of sentences:", num_sentences)
    
    
    from nltk.corpus import cmudict
    #nltk.download('cmudict')
    #Load the CMU Pronouncing Dictionary
    cmu_dict = cmudict.dict()

    # Count the number of complex words
    complex_word_count = 0
    for word in tokens:
        syllable_count = 0
        if word.lower() in cmu_dict:
            # Calculate the number of syllables in the word
            for syllable in cmu_dict[word.lower()][0]:
                if syllable[-1].isdigit():
                    syllable_count += 1
            # Check if the word has more than 2 syllables
            if syllable_count > 2:
                complex_word_count += 1

    #print("Number of complex words:", complex_word_count)
    
    #average sentence length
    average_sentence_length= len(tokens)/num_sentences
    print("average_sentence_length",average_sentence_length)

    #percentage of complex words
    percentage_of_complex_words=complex_word_count/len(tokens)
    print("percentage of complex words",percentage_of_complex_words)

    #fog index
    fog_index=0.4*(average_sentence_length+percentage_of_complex_words)
    print("fog_index",fog_index)
    
    return average_sentence_length, percentage_of_complex_words,fog_index



    


# # 3. Average Number of Words Per Sentence
# 

# In[39]:


def avg_words_per_sentence(tokens):
    #Average Number of Words Per Sentence
    avg_n_words_p_sentence=len(tokens)/num_sentences
    
    print("Average words per sentence",avg_n_words_p_sentence)
    
    return avg_n_words_p_sentence


# # 4. Complex Word Count

# In[40]:


def complex_number(tokens):
        cmu_dict = cmudict.dict()
        # Count the number of complex words
        complex_word_count = 0
        for word in tokens:
            syllable_count = 0
            if word.lower() in cmu_dict:
                # Calculate the number of syllables in the word
                for syllable in cmu_dict[word.lower()][0]:
                    if syllable[-1].isdigit():
                        syllable_count += 1
                # Check if the word has more than 2 syllables
                if syllable_count > 2:
                    complex_word_count += 1

        print("Number of complex words:", complex_word_count)
        return complex_word_count


# # 5. Word Count
# 

# In[41]:


def word_count(text):
    #Word Count
    #from nltk.corpus import stopwords
    #import string
    #nltk.download('stopwords')
    # read the text file

    # convert text to lowercase
    text = text.lower()

    # tokenize the text
    tokens = word_tokenize(text)

    # remove stop words and punctuations
    stop_words = set(stopwords.words('english'))
    global cleaned_tokens
    cleaned_tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]

    # count words
    word_count = len(cleaned_tokens)

    print("Word count:", word_count)
    
    return word_count


# # 6. Syllable Count Per Word
# 

# In[42]:


def syllable_count_per_word(cleaned_tokens):
    

    #Syllable Count Per Word
    # create a syllable tokenizer object
    #from nltk.tokenize import SyllableTokenizer

    syllable_tokenizer = SyllableTokenizer()

    # count the number of syllables in each word
    syllable_counts = []
    for word in cleaned_tokens:
        if word.endswith(('es', 'ed')):
            syllable_counts.append(len(syllable_tokenizer.tokenize(word)) - 1)
        else:
            syllable_counts.append(len(syllable_tokenizer.tokenize(word)))

    # print the number of syllables in each word
    print("Syllable count for each word",syllable_counts)
    
    return syllable_counts


# # 7. Personal Pronouns
# 

# In[43]:


def personal_pronoun(text):
    import re
    text=text.lower()

    # Define the regex pattern for personal pronouns
    pattern = r'\b(I|we|my|ours|us)\b'

    # Find all occurrences of the pattern in the text
    matches = re.findall(pattern, text)

    # Print the count of personal pronouns
    print("Number personal pronouns",len(matches))
    
    return len(matches)


# # 8. Average Word Length

# In[44]:


def avg_w_length(cleaned_tokens):
    t_c_each_word=0
    for word in cleaned_tokens:
        t_c_each_word=t_c_each_word+len(word)
    print("Average Word Length",t_c_each_word/len(cleaned_tokens))
    
    return (t_c_each_word/len(cleaned_tokens))


# # Calling functions 

# # making loop for all text files and getting mentioned output varibles 

# In[45]:


write_list=[]
for i in range(37,151):
    in_list=[]
    file_name=str(i)+".txt"
    print("******************BEGINING OF*************   "+file_name)
    
    #for tokenizing
    
    tokens,text=text_token(file_name)

    #for positive_score
    f1=posit_score(tokens)
    in_list.append(f1)

    #for negative_score
    f2=negat_score(tokens)
    in_list.append(f2)

    #for polarity_score
    f3=polar_score()
    in_list.append(f3)

    #for subjective_score
    f4=subject_score(tokens)
    in_list.append(f4)

    #for analysis of readability
    f5,f6,f7=analysis_readability(text,tokens)
    in_list.append(f5)
    in_list.append(f6)
    in_list.append(f7)

    #for finding avg_words_per_sentence
    f8=avg_words_per_sentence(tokens)
    in_list.append(f8)

    #for finding number of complex words
    f9=complex_number(tokens)
    in_list.append(f9)

    #for finding word count
    f10=word_count(text)
    in_list.append(f10)

    #for finding syllables for each word after perfect cleaning
    f11=syllable_count_per_word(cleaned_tokens)
    in_list.append(f11)
    

    #for finding no.of personal pronouns
    f12=personal_pronoun(text)
    in_list.append(f12)

    #for finding average word length
    f13=avg_w_length(cleaned_tokens)
    in_list.append(f13)
    
    
    
    write_list.append(in_list)
    
    #print(write_list)
    
    print("******************END OF*************   "+file_name)
    


# In[46]:


import csv

# open the CSV file in write mode
with open("Output Data.xlsx - Sheet1.csv", "w", newline="") as file:
    # create a CSV writer object
    writer = csv.writer(file)
    
    # write the values to the file
    writer.writerows(write_list)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




