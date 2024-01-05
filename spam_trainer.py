'''
Spam Trainer: spam_trainer.py
A program to train a Spam Doctor
Created by Peter Leow in Feb 2018 for participating in
Machine Learning and Artificial Intelligence Challenge
organized by CodeProject
'''

import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter
import pandas as pd
import csv
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

# +++++ functions +++++

def txt2List(fileName): # read text file to list
    with open(fileName) as file:
        # Make each message an element of a list
        return list(file)

def tokenize(dataset):

    # Convert all letters to lowercase
    temp1 = [message.lower() for message in dataset]
    # print(temp1[-1], end='\n\n')

    # Relegate each unwanted word to a whitespace
    temp2 = [message.replace('<p>', ' ').replace('</p>', ' ').replace('<a href="https://', ' ').replace('">', ' ').replace('</a>', ' ') for message in temp1]

    # Break each message into tokens of word
    temp3 = [ word_tokenize(message) for message in temp2 ]

    # Remove duplicate tokens in each message
    temp4 = [ set(element) for element in temp3 ]
    # print(temp4[-1], end='\n\n')

    # Remove tokens of stop words and punctuation
    stopWords = set(stopwords.words('english'))
    stopWords.update(string.punctuation)

    finalDataset = []

    for tokenList in temp4:
        temp5 = []
        for token in tokenList:
            if token not in stopWords:
                temp5.append(token)
        finalDataset.append(temp5)
    
    return finalDataset

def tokenConditionalProbability(dataset):

    # Number of samples in dataset
    sampleSize = len(dataset)

    # Dictionary of token-probability pairs
    conditionalProbabilities = {}

    # Count probability of occurence of each token
    flatten = []
    flatten[len(flatten):] = [ token for sample in dataset for token in sample ]
    tokenCount = Counter(flatten)
    conditionalProbabilities = { key : value / sampleSize for key, value in tokenCount.items()}        

    return conditionalProbabilities

def spamPosteriorProbability(tokenList):
    spamTokenConditionalProbability = 1
    hamTokenConditionalProbability = 1
    for token in tokenList:
            
        if token not in spamTokensConditionalProbabilities:
            spamTokenConditionalProbability *= 0.01 # To minimize false positive
        else:
            spamTokenConditionalProbability *= spamTokensConditionalProbabilities[token]
            
        if token not in hamTokensConditionalProbabilities:
            hamTokenConditionalProbability *= 0.01 # To mininize false negative
        else:
            hamTokenConditionalProbability *= hamTokensConditionalProbabilities[token]    

    return spamTokenConditionalProbability * spamPriorProbability / (spamTokenConditionalProbability * spamPriorProbability + hamTokenConditionalProbability * hamPriorProbability)    

# +++++ Learning +++++

spamMessages = [ (re.search('(?<=Spam,<p>).*(?=</p>)', element)).group(0) for element in txt2List('spam2.txt') ]
# print(len(spamMessages), end='\n\n')

hamMessages = [ (re.search('(?<=Ham,<p>).*(?=</p>)', element)).group(0) for element in txt2List('ham2.txt') ]
# print(len(hamMessages), end='\n\n')

# The prior probability of a message is spam
spamPriorProbability = len(spamMessages) / (len(spamMessages) + len(hamMessages))

# The prior probability of a message is ham
hamPriorProbability = len(hamMessages) / (len(spamMessages) + len(hamMessages))

# Turn each message into a list of tokens
spamTokens = tokenize(spamMessages)
hamTokens = tokenize(hamMessages)

# Calculate the conditional probability of individual token in spam and ham respectively
spamTokensConditionalProbabilities = tokenConditionalProbability(spamTokens) # Dictionary
hamTokensConditionalProbabilities = tokenConditionalProbability(hamTokens) # Dictionary
# print(spamTokensConditionalProbabilities, end='\n\n')
# print(hamTokensConditionalProbabilities, end='\n\n')

# +++++ Testing +++++

testSet = txt2List('test2.txt')
# print(len(testSet))
testMessages = [ (re.search('(?<=[Sp|H]am,<p>).*(?=</p>)', element)).group(0) for element in testSet ]
testTokens = tokenize(testMessages)

spamPosteriorProbability = [ spamPosteriorProbability(tokenList) for tokenList in testTokens ]

truePositive = falseNegative = falsePositive = trueNegative = 0

threshold = 0.8

for data, spamPosteriorProbability in zip(testSet, spamPosteriorProbability):
    expected = data.split(',')[0]
    if expected == 'Spam':
        if spamPosteriorProbability > threshold:
            truePositive += 1
        else:
            falseNegative += 1
    elif expected == 'Ham':
        if spamPosteriorProbability > threshold:
            falsePositive += 1
        else:
            trueNegative += 1

print('{0} = {1}'.format('True Positive', truePositive))
print('{0} = {1}'.format('False Negative', falseNegative))
print('{0} = {1}'.format('False Positive', falsePositive))
print('{0} = {1}'.format('True Negative', trueNegative))
print()

# +++++ Confusion Matrix +++++

d = {'Tested Spam' : pd.Series([truePositive, falsePositive, truePositive + falsePositive], index=['Expected Spam','Expected Ham', 'Total'])}
df = pd.DataFrame(d)
df['Tested Ham'] = pd.Series([falseNegative, trueNegative, falseNegative + trueNegative], index=['Expected Spam','Expected Ham', 'Total'])
df['Total'] = pd.Series([truePositive + falseNegative, falsePositive + trueNegative, truePositive + falseNegative + falsePositive + trueNegative], index=['Expected Spam','Expected Ham', 'Total'])
print('                  Confusion Matrix')
print(df)

print()

print('Accuracy =', (truePositive + trueNegative)/len(testSet) * 100, '%')
print('Precision =', truePositive / (truePositive + falsePositive) * 100, '%')

# +++++ Save the learned knowledge to CSV files +++++

with open('spamTokensConditionalProbabilities.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in spamTokensConditionalProbabilities.items():
        writer.writerow([key, value])

with open('hamTokensConditionalProbabilities.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in hamTokensConditionalProbabilities.items():
        writer.writerow([key, value])

with open('parameters.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['spamPriorProbability', spamPriorProbability])
    writer.writerow(['hamPriorProbability', hamPriorProbability])
    writer.writerow(['threshold', threshold])
