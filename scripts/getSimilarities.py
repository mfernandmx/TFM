#!/usr/bin/python
# -*- coding: utf-8 -*-

# Gensim
import gensim
import gensim.corpora as corpora
# from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# Plotting tools
# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt

from random import uniform

# Enable logging for gensim - optional
import logging
import warnings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

mallet_path = './mallet-2.0.8/bin/mallet'

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
	""" Compute c_v coherence for various number of topics

	Parameters:
	----------
	dictionary : Gensim dictionary
	corpus : Gensim corpus
	texts : List of input texts
	limit : Max num of topics

	Returns:
	-------
	model_list : List of LDA topic models
	coherence_values : Coherence values corresponding to the LDA model with respective number of topics
	"""

	coherence_values = []
	model_list = []

	for num_topics in range(start, limit, step):
		model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
		model_list.append(model)
		coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
		coherence_values.append(coherencemodel.get_coherence())

	return model_list, coherence_values

def getLikenessValue(tokens1, tokens2):
	# key_words = ["uri","http","recurso","opendata"]
	# doc_a = dataset1.title + " " + dataset1.identifier + " " + str(dataset1.keyword) + " " + dataset1.theme + " " + dataset1.description

	# print(doc_a)

	# texts = getTokens(doc_a)

	dictionary1 = corpora.Dictionary([tokens1])
	print(dictionary1.token2id)

	corpus1 = [dictionary1.doc2bow(text) for text in [tokens1]]

	print(corpus1[0])

	#
	# Create Dictionary
	id2word = corpora.Dictionary([tokens1])

	# Create Corpus
	texts = [tokens1]

	# Term Document Frequency
	corpus = [id2word.doc2bow(text) for text in texts]

	ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=20, id2word=id2word)

	# Show Topics

	print(ldamallet.show_topics(formatted=False))
	# Compute Coherence Score
	coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=texts, dictionary=id2word, coherence='c_v')
	coherence_ldamallet = coherence_model_ldamallet.get_coherence()
	print('\nCoherence Score: ', coherence_ldamallet)

	# Can take a long time to run.

	model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=texts, start=2, limit=20, step=2)

	print("coherence: ", coherence_values)
	# Show graph
	limit = 20
	start = 2
	step = 2
	x = range(start, limit, step)
	plt.plot(x, coherence_values)
	plt.xlabel("Num Topics")
	plt.ylabel("Coherence score")
	plt.legend("coherence_values", loc='best')
	plt.show()

	# Print the coherence scores
	for m, cv in zip(x, coherence_values):
		print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

	ldamodel1 = gensim.models.ldamodel.LdaModel(corpus1, num_topics=3, id2word=dictionary1, passes=20)
	ldamodel2 = gensim.models.ldamodel.LdaModel(corpus1, num_topics=2, id2word=dictionary1, passes=20)

	dictionary2 = corpora.Dictionary([tokens2])
	print(dictionary2.token2id)

	corpus2 = [dictionary2.doc2bow(text) for text in [tokens2]]

	print(corpus2[0])

	ldamodel3 = gensim.models.ldamodel.LdaModel(corpus2, num_topics=3, id2word=dictionary2, passes=20)
	ldamodel4 = gensim.models.ldamodel.LdaModel(corpus2, num_topics=2, id2word=dictionary2, passes=20)

	print(ldamodel1.print_topics(num_topics=3, num_words=5))
	print(ldamodel2.print_topics(num_topics=2, num_words=5))
	print(ldamodel3.print_topics(num_topics=3, num_words=5))
	print(ldamodel4.print_topics(num_topics=2, num_words=5))

	print(" ")
	print("******************************************")
	print(" ")

	return uniform(0.0, 1.0)
