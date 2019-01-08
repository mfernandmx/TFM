#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from scripts.normalizer import normalize

# LDA proccess
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer

# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

'''
Given a string, return true if it contains numbers. False if not
'''
def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))


'''
Given a set of words, it process them in order to have a new set of tokens based on those previous words, resultant from
delete numbers, stop words, urls, ontologies, sparql queries, and also removing gender and number from the words, getting
only the words' lexemes
'''
def tokenize(data):
	# URLs, properties and sparql queries are removed
	text = re.sub(r'http.+', '', data)
	text = re.sub(r'\w+:\w+', '', text)
	text = re.sub(r'\?\w+', '', text)

	# Tokenize and normalize the tokens
	tokenizer = RegexpTokenizer(r'\w+')
	tokenized = text.split(" ")

	aux = [normalize(token) for token in tokenized]
	tokens = tokenizer.tokenize(str(aux))

	# Stop words are removed (stop words such as prepositions)
	aux = [i for i in tokens if i not in stop_words]

	# Numbers are removed
	noNumbers = [i for i in aux if not hasNumbers(str(i))]

	# Removing gender and number from words
	p_stemmer = SnowballStemmer('english')
	tokens = [p_stemmer.stem(i) for i in noNumbers]

	return tokens
