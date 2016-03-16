# -*- coding: utf-8 -*-
from nltk.tokenize import TweetTokenizer
import HTMLParser
html_parser = HTMLParser.HTMLParser()

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)


import re

# myre = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u26FF\u2700-\u27BF])+', re.UNICODE)


# regex = re.compile(r'\w\1\1')

# all_words = set(get_all_words())

# def without_elongations(word):
#     while re.search(regex, word) is not None:
#         replacing_with_one_letter = re.sub(regex, r'\1', word, 1)
#         replacing_with_two_letters = re.sub(regex, r'\1\1', word, 1)
#         return list(itertools.chain(
#             without_elongations(replacing_with_one_letter),
#             without_elongations(replacing_with_two_letters),
#         ))


def has_long(sentence):
    elong = re.compile("([a-zA-Z])\\1{2,}")
    return bool(elong.search(sentence))


# for word in sentence.split():
#     if word not in all_words:
#         if any(map(lambda w: w in all_words, without_elongations(word)):
#             print('%(word) is elongated', { 'word': word })

def clean(text):
	text=html_parser.unescape(text)
	# print text
	# text.decode("utf8")
	# print text
	# text=re.sub(r"http\S+", "", text)
	# text=" ".join(re.findall('[A-Z][^A-Z]*', text))
	tl=tknzr.tokenize(text)
	newtext=""
	for t in tl:
		# t = unicode(t, 'utf-8')
		t = t.encode('unicode_escape');
		if t=="\ud83c" or t=="\ud83d" or t[0:4]=="\u26" :
		# or (t[0:4]=="\u27" and int(t[4:6],16)>=int("00",16) and int(t[4:6],16)<=int("BF",16)):
			newtext+=unicode(t)
		else:
			newtext+=unicode(t)+" "

	# newtext = newtext.encode('unicode_escape');
	# newtext = myre.sub('lulululu', newtext)

	print newtext
	return newtext

s="I'm 💩😃:) looooooool in❤ \tyy???!"


# for word in clean(s).split():
#     if word not in all_words:
#         if any(map(lambda w: w in all_words, without_elongations(word))):
#             print('%(word) is elongated', { 'word': word })

print has_long(clean(s))
