# -*- coding: utf-8 -*-
from pandas import read_csv
from nltk.tokenize import TweetTokenizer
import HTMLParser
html_parser = HTMLParser.HTMLParser()
from sklearn.svm import SVC
from sklearn import cross_validation
import re
from numpy import array
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
import numpy
numpy.set_printoptions(threshold=numpy.nan)

prs=open('personal.txt','r')
sml=open('smile.txt','r')
stng=open('strong_subj.txt','r')

personal=[]
smileys=[]
strongsubj=[]


for p in prs:
	personal.append(p.rstrip())
for sm in sml:
	smileys.append(sm.rstrip())
for sj in stng:
	strongsubj.append(sj.rstrip())

personal=set(personal)
smileys=set(smileys)
strongsubj=set(strongsubj)



def clean(text):
	# text=html_parser.unescape(text)
	tl=tknzr.tokenize(text)
	newtext=""
	for t in tl:
		t = t.encode('unicode_escape');
		t=t.lower()
		# if t not in stop_words:
		if t=="\ud83c" or t=="\ud83d" or t[0:4]=="\u26" :
			# or (t[0:4]=="\u27" and int(t[4:6],16)>=int("00",16) and int(t[4:6],16)<=int("BF",16)):
			newtext+=t
		else:
			newtext+=t+" "

	return newtext

def has_long(sentence):
    elong = re.compile("([a-zA-Z])\\1{2,}")
    if bool(elong.search(sentence)):
    	return 1
    else:
    	return 0

def has_personal(sentence):
	for w in sentence.split(" "):
		if w in personal:
			return 1
			break
	return 0

def has_smiley(sentence):
	for w in sentence.split(" "):
		if w in smileys:
			return 1
			break
	return 0

def has_strong(sentence):
	for w in sentence.split(" "):
		if w in strongsubj:
			return 1
			break
	return 0

def has_q(sent):
	if '?' in sent.split(" "):
		return 1
	else:
		return 0

def has_ex(sent):
	if '!' in sent.split(" "):
		return 1
	else:
		return 0

def has_emoji(sent):
	for t in sent.split(" "):
		if t=="\ud83c" or t=="\ud83d" or t[0:4]=="\u26" :
			return 1
			break
	return 0




df = read_csv('labelledtweets_2.csv')


text=[]
tag=[]

for i,r in df.iterrows():
	tx=r['text']
  	clean(tx)
	text.append(tx)
	# print clean(tx)
	if r['tag']==2:
		tag.append(1) #obj
	else:
		tag.append(2) #subj


label=array(tag)

textlist=[]
for s in text:
	textlist.append([has_emoji(s), has_ex(s),has_q(s),has_strong(s),has_smiley(s),has_personal(s),has_long(s)])

feature=array(textlist)
# print feature

trainclf = SVC(kernel='rbf',gamma=0.5)
trainclf.fit(feature, label)


#CROSS VALIDATION

feature_train, feature_test, label_train, label_test = cross_validation.train_test_split(feature, label, test_size=0.1, random_state=0)
print trainclf.score(feature_test, label_test) 

# from sklearn.externals import joblib
# # # now you can save it to a file
# joblib.dump(trainclf, 'savedclassifier.pkl')

# # and later you can load it
# trainclf = joblib.load('savedclassifier.pkl')

# scores = cross_validation.cross_val_score(trainclf, feature, label,CV=10)
# print scores.mean(), scores.std()


#Testing

# testdf=read_csv('unlabelledtweets_2.csv')

# testtext=[]
# testtag=[]
# testlist=[]

# for i,r in testdf.iterrows():
# 	tsttx=r['text']
# 	try:
#   		clean(tsttx)
# 	except: 
#   		pass
# 	testtext.append(tsttx)

# for s in testtext:
# 	testlist.append([has_emoji(s), has_ex(s),has_q(s),has_strong(s),has_smiley(s),has_personal(s),has_long(s)])

# testtag=trainclf.predict(testlist)
# # print testtag.tolist()

# import csv
# from itertools import izip

# with open('output.csv', 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(izip(testtext, testtag.tolist()))




