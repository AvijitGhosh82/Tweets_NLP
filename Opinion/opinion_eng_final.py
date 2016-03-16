# -*- coding: utf-8 -*-
# from xlrd import open_workbook
from nltk.tokenize import TweetTokenizer
import HTMLParser
html_parser = HTMLParser.HTMLParser()
from pattern.en import parsetree
from sklearn.svm import SVC
from sklearn import cross_validation
import re
from numpy import array
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
import numpy
numpy.set_printoptions(threshold=numpy.nan)
import codecs


import warnings
warnings.filterwarnings("ignore")

import pyexcel
import pyexcel.ext.xlsx

prs=open('personal.txt','r')
sml=open('smile.txt','r')
stng=open('strong_subj.txt','r')
weakf=open('weak_subj.txt','r')
whw=open('wh.txt','r')
slang=open('eng_slang.txt','r')
modal=open('modal.txt','r')
nrc=codecs.open("NRC-Hashtag-Emotion-Lexicon-v0.2.txt",'r','utf-8')

nrcdict={}

###GETTING NRC

for line in nrc:
	nrcdict[line.split()[1]]=float(line.split()[2])

def getnrcscore(line):
	# print("In nrc")
	line.lower()
	score=0
	for w in line:
		if w in nrcdict.keys():
			score+=nrcdict.get(w)
	# print("out nrc")
	return score

personal=[]
smileys=[]
strongsubj=[]
modall=[]
slangll=[]
whll=[]
weaksubj=[]


for p in prs:
	personal.append(p.rstrip())
for sm in sml:
	smileys.append(sm.rstrip())
for sj in stng:
	strongsubj.append(sj.rstrip())
for m in modal:
	modall.append(m.rstrip())
for s in slang:
	slangll.append(s.rstrip())
for w in whw:
	whll.append(w.rstrip())
for wk in weakf:
	weaksubj.append(w.rstrip())

personal=set(personal)
smileys=set(smileys)
strongsubj=set(strongsubj)
weaksubj=set(weaksubj)


def has_upper(text):
	for w in text.split():
		if w.isupper():
			return 1
	# print("out upper")
	return 0

def clean(text):
	# text=html_parser.unescape(text)
	tl=tknzr.tokenize(text)
	newtext=""
	# newtext=tl
	for t in tl:
		# t = t.encode('unicode_escape');
		t=t.lower()
		# if t not in stop_words:
		# if t=="\ud83c" or t=="\ud83d" or t[0:4]=="\u26" :
		# 	# or (t[0:4]=="\u27" and int(t[4:6],16)>=int("00",16) and int(t[4:6],16)<=int("BF",16)):
		# 	newtext+=t
		# else:
		newtext+=t+" "
	# print newtext
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

def has_modal(sentence):
	for w in sentence.split(" "):
		if w in modall:
			return 1
			break
	return 0

def has_wh(sentence):
	for w in sentence.split(" "):
		if w in whll:
			# print sentence
			return 1
			break
	return 0

def has_slang(sentence):
	for w in sentence.split(" "):
		if w in slangll:
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

def has_weak(sentence):
	for w in sentence.split(" "):
		if w in weaksubj:
			return 1
			break
	return 0

def has_q(sent):
	if '?' in sent:
		# print sent
		return 1
	else:
		return 0

def has_ex(sent):
	if '!' in sent:
		# print sent
		return 1
	else:
		return 0

def has_emoji(sent):
	for t in sent.split(" "):
		if t=="\ud83c" or t=="\ud83d" or t[0:4]=="\u26" :
			return 1
			break
	return 0


def has_double_highlight(line):
	match=re.search(r'\"(.+?)\"',line)
	if match:
		quote=match.group()[1:-1]
		s=parsetree(quote,chunk =True ,relations=True, lemmata=True)
		for sentence in s:
			rel= sentence.relations
			pnp= sentence.pnp
			sbj=True
			vb=True
			obj=True
			pnp=True

			if not rel.get("SBJ"): 
				sbj=False
			if not rel.get("VP"): 
				vp=False
			if not rel.get("OBJ"): 
				obj=False
			if not pnp: 
				pnp=False

			if sbj and vb and (obj or pnp):
				# quotes.append(line)
				return 0
			else:
				return 1
	else:
		return 0

def has_single_highlight(line):
	match=re.search(r'\'(.+?)\'',line)
	if match:
		quote=match.group()[1:-1]
		s=parsetree(quote,chunk =True ,relations=True, lemmata=True)
		for sentence in s:
			rel= sentence.relations
			pnp= sentence.pnp
			sbj=True
			vb=True
			obj=True
			pnp=True

			if not rel.get("SBJ"): 
				sbj=False
			if not rel.get("VP"): 
				vp=False
			if not rel.get("OBJ"): 
				obj=False
			if not pnp: 
				pnp=False

			if sbj and vb and (obj or pnp):
				# quotes.append(line)
				return 0
			else:
				return 1
	else:
		return 0




# df = read_csv('labelledtweets_2.csv')

# values = []

# for s in wb.sheets():
# 	#print 'Sheet:',s.name
#     for row in range(1, s.nrows):
#         col_names = s.row(0)
#         col_value = []
#         for name, col in zip(col_names, range(s.ncols)):
#             value  = (s.cell(row,col).value)
#             try : value = str(int(value))
#             except : pass
#             col_value.append((name.value, value))
#         values.append(col_value)

text=[]
utext=[]
tag=[]

# for tweet in values:
# 	# tx=tweet[0]
# 	# print tx
# 	# clean(tx)
# 	# text.append(tx)
# 	# tg=tweet[1][1]
# 	# tag.append(tg)
# 	for i in tweet:
# 		print i
# 	print "\n"

trainclf = SVC(kernel='rbf',gamma=0.5)

sc=0
fulltext=[]
fullutext=[]
fulltag=[]
book = pyexcel.get_book(file_name="English_Train-final.xlsx")
for sheet in book:
	if sc==3:
		break
	
	data=pyexcel.to_array(sheet.rows())
	text=[]
	utext=[]
	tag=[]
	for tweet in data:
		tx=tweet[0]
		tx=clean(tx)
		utext.append(tweet[0])
		text.append(tx)
		tag.append(tweet[1])
		fullutext.append(tweet[0])
		fulltext.append(tx)
		fulltag.append(tweet[1])

	# for i,r in df.iterrows():
	# 	tx=r['text']
	#   	clean(tx)
	# 	text.append(tx)
	# 	# print clean(tx)
	# 	if r['tag']==2:
	# 		tag.append(1) #obj
	# 	else:
	# 		tag.append(2) #subj


# getnrcscore(s)
	label=array(tag)

	textlist=[]
	c=0
	for s in text:
		# textlist.append([has_modal(s),has_strong(s),has_personal(s),has_long(s), has_wh(s)])
		textlist.append([has_emoji(s),has_modal(s),has_ex(s),has_q(s),has_strong(s),has_weak(s),has_smiley(s),has_personal(s),has_long(s), has_wh(s), has_slang(s),has_upper(utext[c]),has_single_highlight(s), has_double_highlight(s)])
		c=c+1

	feature=array(textlist)
	# print feature

	trainclf.fit(feature, label)


	# print "CROSS VALIDATION"

	score = cross_validation.cross_val_score(trainclf, feature, label,cv=10)
	print score.mean(), score.std()
	sc+=1

	# feature_train, feature_test, label_train, label_test = cross_validation.train_test_split(feature, label, test_size=0.1, random_state=0)
	# print trainclf.score(feature_test, label_test) 



fulllabel=array(fulltag)

fulltextlist=[]
c=0
for s in fulltext:
		# textlist.append([has_modal(s),has_strong(s),has_personal(s),has_long(s), has_wh(s)])
	fulltextlist.append([has_emoji(s),has_modal(s),has_ex(s),has_q(s),has_strong(s),has_weak(s),has_smiley(s),has_personal(s),has_long(s), has_wh(s), has_slang(s),has_upper(fullutext[c]),has_single_highlight(s), has_double_highlight(s)])
	c=c+1

fullfeature=array(fulltextlist)

fulltrainclf = SVC(kernel='rbf',gamma=0.5)

	# print feature

fulltrainclf.fit(fullfeature, fulllabel)

sheet=book[3]


data=pyexcel.to_array(sheet.rows())
text=[]
utext=[]
tag=[]
for tweet in data:
	tx=tweet[0]
	tx=clean(tx)
	utext.append(tweet[0])
	text.append(tx)

textlist=[]
c=0
for s in text:
	# textlist.append([has_modal(s),has_strong(s),has_personal(s),has_long(s), has_wh(s)])
	textlist.append([has_emoji(s),has_modal(s),has_ex(s),has_q(s),has_strong(s),has_weak(s),has_smiley(s),has_personal(s),has_long(s), has_wh(s), has_slang(s),has_upper(utext[c]),has_single_highlight(s), has_double_highlight(s)])
	c=c+1

feature=array(textlist)


	# print feature

pred= fulltrainclf.predict(feature)

one_as_2=0
two_as_one=0

c=0
a=[]
for tweet in data:
	a.append ([tweet[0], tweet[1], pred[c]])
	if tweet[1]==1 and pred[c]==2 :
		one_as_2+=1
	elif tweet[1]==2 and pred[c]==1 :
		two_as_one+=1
	c+=1

sheet = pyexcel.Sheet(a)
sheet.save_as("error.csv")
print "One as Two: ", one_as_2
print "Two as One: ",two_as_one


