#Python 2.x program to transcribe an Audio file

import tkinter
import tkinter.filedialog
from tkinter import *

root = tkinter.Tk()
f=''
def print_path():
    global f
    f = tkinter.filedialog.askopenfilename(
        parent=root, initialdir='C:/Tutorial',
        title='Choose file',
        filetypes=[('audio files', '.wav')]
        )

#print(f)

b1 = tkinter.Button(root, text='upload', command=print_path)
b1.pack(fill='x')
Button(root, text="Done", command=root.destroy).pack()
root.mainloop()


import speech_recognition as sr

AUDIO_FILE = (f)

# use the audio file as the audio source

r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
	#reads the audio file. Here we use record instead ofe
	#listen
	audio = r.record(source)

try:
	print("The audio file contains: " + r.recognize_google(audio))
	aud_ip = r.recognize_google(audio)
	#print(type(aud_ip))

except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")

except sr.RequestError as e:
	print("Could not request results from Google Speech Recognition service; {0}".format(e))

'''
Spam Doctor: spam_doctor.py
An GUI app for diagnosing if a new message is spam
Created by Peter Leow in Feb 2018 for participating in
Machine Learning and Artificial Intelligence Challenge
organized by CodeProject
'''

from tkinter import *
from tkinter import messagebox
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# +++++ functions +++++

def tokenize(message):

    # Convert all letters to lowercase
    temp1 = message.lower()

    # Relegate each unwanted word to a whitespace
    temp2 = temp1.replace('<p>', ' ').replace('</p>', ' ').replace('<a href="https://', ' ').replace('">', ' ').replace('</a>', ' ')

    # Break each message into tokens of word
    temp3 = word_tokenize(temp2)

    # Remove duplicate tokens in each message
    temp4 = set(temp3)

    # Remove tokens of stop words and punctuations
    stopWords = set(stopwords.words('english'))
    stopWords.update(string.punctuation)

    tokenizedMessage = []

    for token in temp4:
        if token not in stopWords:
            tokenizedMessage.append(token)

    return tokenizedMessage

list_of_words=['Act now', '100% free','ad','apply now','guarantee','order','leave','web traffic','weight loss','free gift','credit','cheap','billion','amazing stuff','promise you','save','free offer','stop','fast cast','free membership','no investment',
'refinance','save $','order now','order today','opportunity','search engine','refinance','save $','order today','Apply now','Guarantee','leave','web traffic','weight loss',
'free gift','credit','cheap','billion','amazing stuff','promise you','save','unsubscribe','free offer','stop','save','fast cash','free membership','web traffic','cash bonus',
'no investment','opportunity','pin','otp','cvv','search engine','refinance','save $','Order now','order todayo investment','opportunity','search engine','refinance','save $','Order now','order todayo investment','opportunity','search engine','refinance','save $','Order now','order today']

def getSpamPosteriorProbability(tokenList):
    spamTokenConditionalProbability = 1
    hamTokenConditionalProbability = 1
    for token in tokenList:

        if token not in spamTokensConditionalProbabilities:
            spamTokenConditionalProbability *= 0.01 # To minimize false positive
        else:
            spamTokenConditionalProbability *= float(spamTokensConditionalProbabilities[token])

        if token not in hamTokensConditionalProbabilities:
            hamTokenConditionalProbability *= 0.01 # To mininize false negative
        else:
            hamTokenConditionalProbability *= float(hamTokensConditionalProbabilities[token])

    return spamTokenConditionalProbability * float(parameters['spamPriorProbability']) / (spamTokenConditionalProbability * float(parameters['spamPriorProbability']) + hamTokenConditionalProbability * float(parameters['hamPriorProbability']))

def diagnose():
    flag = 0
    pin="pin"
  # aud_ip2=aud_ip+pin
    input = aud_ip
   # input = pin

    if input.strip() == '':
        return

    for x in range(len(list_of_words)):
        if list_of_words[x] in input:
            messagebox.showinfo("prior by srujan", "You've got spam!")
            flag = flag + 1
            break
        else:
            continue




#    '''elif input.find("pin") >= 0:
 #       messagebox.showinfo("Dignosis", "You've got spam!")'''


    tokenList = tokenize(input)

    spamPosteriorProbability = getSpamPosteriorProbability(tokenList)

    if spamPosteriorProbability > float(parameters['threshold']):
        if flag != 1:
            messagebox.showinfo("Dignosis", "You've got spam!")
    else:
        if flag != 1:
            messagebox.showinfo("Diagnosis", "You are in good ham. Oops! I mean good health.")

spamTokensConditionalProbabilities = {}
hamTokensConditionalProbabilities = {}
parameters = {}

# +++++ Load the knowledge from CSV files +++++

with open('spamTokensConditionalProbabilities.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        spamTokensConditionalProbabilities[row[0]] = row[1]

with open('hamTokensConditionalProbabilities.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        hamTokensConditionalProbabilities[row[0]] = row[1]

with open('parameters.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        parameters[row[0]] = row[1]

# +++++ GUI +++++

root = Tk()
root.title("Spam Doctor")

label = Label(root, text="click here")
label.pack()

#msgbox = Text(root, height=20, width=80)
#msgbox.pack()

btnDiagnose = Button(root, height=1, width=10, text="Diagnose", command=diagnose)

btnDiagnose.pack()

root.mainloop()
