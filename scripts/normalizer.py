#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Given a word, it removes all the characters that contains accent marks or any other symbol
"""
def normalize(word):

	result = word.lower()
	result = result.replace(u'á', u'a')
	result = result.replace(u'ά', u'a')
	result = result.replace(u'é', u'e')
	result = result.replace(u'í', u'i')
	result = result.replace(u'ó', u'o')
	result = result.replace(u'ú', u'u')
	result = result.replace(u'à', u'a')
	result = result.replace(u'è', u'e')
	result = result.replace(u'ì', u'i')
	result = result.replace(u'ò', u'o')
	result = result.replace(u'ù', u'u')
	result = result.replace(u'â', u'a')
	result = result.replace(u'ê', u'e')
	result = result.replace(u'î', u'i')
	result = result.replace(u'ô', u'o')
	result = result.replace(u'û', u'u')
	result = result.replace(u'ä', u'a')
	result = result.replace(u'ë', u'e')
	result = result.replace(u'ì', u'i')
	result = result.replace(u'ò', u'o')
	result = result.replace(u'ù', u'u')
	result = result.replace(u'ș', u's')
	result = result.replace(u'Ç', u'c')
	result = result.replace(u'ĉ', u'c')
	result = result.replace(u'č', u'c')
	result = result.replace(u'ñ', u'n')
	result = result.replace(u'Ù', u'u')
	result = result.replace(u'Û', u'u')
	result = result.replace(u'Ü', u'u')
	result = result.replace(u'Þ', u'b')
	result = result.replace(u'ß', u'ss')
	result = result.replace(u'Ð', u'd')
	result = result.replace(u'Ĵ', u'j')
	result = result.replace(u'ĵ', u'j')
	result = result.replace(u'ά', u'a')
	result = result.replace(u'Ÿ', u'y')
	result = result.replace(u'ƒ', u'f')
	result = result.replace(u'_', u'')
	result = result.replace(u'-', u'')
	result = result.replace(u'\n', u'')
	result = result.replace(u'\r', u'')
	result = result.replace(u'\t', u'')

	return result
