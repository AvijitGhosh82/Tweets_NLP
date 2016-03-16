# -*- coding: utf-8 -*-

import re
import codecs
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import SVC
from sklearn import cross_validation
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
import collections
from numpy import array

import pyexcel
import pyexcel.ext.xlsx


# f=codecs.open("tweetdata/training_set.txt",'r','utf-8') 
#Training set too big, reduced to 500
# f=codecs.open("tweetdata/training_set.txt",'r','utf-8')

#CMU TAGGER NEEDS TO BE RUN FOR POSTAGGER

posf=codecs.open("tweetdata/postagged.txt",'r','utf-8')
nrc=codecs.open("lexicon/NRC-Hashtag-Emotion-Lexicon-v0.2.txt",'r','utf-8')
emo=codecs.open("lexicon/EmoticonSentimentLexicon.txt",'r','utf-8')
s140_1=codecs.open("lexicon/s140_1.txt",'r','utf-8')
s140_2=codecs.open("lexicon/s140_2.txt",'r','utf-8')
s140_an_1=codecs.open("lexicon/S140-AFFLEX-NEGLEX-unigrams.txt",'r','utf-8')
s140_an_2=codecs.open("lexicon/S140-AFFLEX-NEGLEX-bigrams.txt",'r','utf-8')
# tweetfile=codecs.open("tweetfile.txt",'w','utf-8')



sentences=[]
tags=[]
pos=[]

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

# for line in f:
# 	l=line.split("\t")
# 	sentences.append(l[3])
# 	print >> tweetfile, l[3]
# 	tags.append(l[2][1:-1]) #objective OR Neutral as CAT 5

# bintag=[]
# for t in tags:
# 	if( t=="positive"):
# 		bintag.append(0)
# 	elif(t=="negative"):
# 		bintag.append(1)
# 	elif(t=="neutral"):
# 		bintag.append(2)
# 	elif(t=="objective-OR-neutral"):
# 		bintag.append(2)
# 	elif(t=="objective"):
# 		bintag.append(3)


# lb = MultiLabelBinarizer()
# Y = lb.fit_transform(tags)

# Y=array(bintag)

# print Y

tws=posf.read().split("\n\n\n")
for tw in tws:
	sent=''
	plist=[]
	l=tw.split('\n')
	for t in l:
		if t:
			sent+=t.split('\t')[0]+' '
			plist.append(t.split('\t')[1])
	# sentences.append(sent.strip())
	pos.append(plist)






# print Y



data=[]
nrcdict={}
emodict={}
s140_uni={}
s140_bi={}
s140_an_uni={}
s140_an_bi={}

###GETTING NRC

for line in nrc:
	nrcdict[line.split()[1]]=float(line.split()[2])

def has_long(sentence):
	# print("In haslong")
	elong = re.compile("([a-zA-Z])\\1{2,}")
	if bool(elong.search(sentence)):
		# print("out haslong")
		return 1
	else:
		# print("out haslong")
		return 0

def getnrcscore(line):
	# print("In nrc")
	line.lower()
	score=0
	for w in line:
		if w in nrcdict.keys():
			score+=nrcdict.get(w)
	# print("out nrc")
	return score


for line in emo:
	emodict[line.split('\t')[0]]=int(line.split('\t')[1])


def getemoscore(line):
	score=0
	for w in line:
		if w in emodict.keys():
			score+=emodict.get(w)
	# print("out emo")
	return score

for line in s140_1:
	s140_uni[line.split('\t')[0]]=float(line.split('\t')[1])

for line in s140_2:
	s140_bi[line.split('\t')[0]]=float(line.split('\t')[1])

for line in s140_an_1:
	s140_an_uni[line.split('\t')[0]]=float(line.split('\t')[1])

for line in s140_an_2:
	s140_an_bi[line.split('\t')[0]]=float(line.split('\t')[1])

def smart_find(needle,haystack):
	if haystack.startswith(needle+" "):
		return True
	if haystack.endswith(" "+needle):
		return True
	if haystack.find(" "+needle+" ") != -1:
		return True
	return False

def gets140_uni(line):
	sc = collections.namedtuple('score', ['tot', 'max','last'])
	score=[]
	for w in line:
		if w in set(s140_uni.keys()):
			score.append(s140_uni.get(w))
	s=sc(0,0,0);
	if (score):
		s=sc(sum(score),max(score),score[-1])
	return s

def gets140_bi(line):
	sc = collections.namedtuple('score', ['tot', 'max','last'])
	score=[]
	for w in set(s140_bi.keys()):
		if smart_find(w,line):
			score.append(s140_bi.get(w))
	s=sc(0,0,0);
	if (score):
		s=sc(sum(score),max(score),score[-1])
	return s

def gets140_an_uni(line):
	try:
		line=replacenegation_monogram(line)
	except Exception, e:
		# raise e
		pass
	sc = collections.namedtuple('score', ['tot', 'max','last'])
	score=[]
	for w in line:
		if w in set(s140_an_uni.keys()):
			score.append(s140_an_uni.get(w))
	s=sc(0,0,0);
	if(score):
		s=sc(sum(score),max(score),score[-1])
	return s


def gets140_an_bi(line):
	try:
		line=replacenegation_bigram(line)
	except Exception, e:
		# raise e
		pass
	score=[]
	sc = collections.namedtuple('score', ['tot', 'max','last'])
	for w in set(s140_an_bi.keys()):
		if smart_find(w,line):
			score.append(s140_an_bi.get(w))
					# print w
	s=sc(0,0,0);
	if (score):
		s=sc(sum(score),max(score),score[-1])
	return s

# def getTweets():
# 	flist = f.read().split("\n\n")
# 	for t in flist:
# 		tlist=t.split('\n')
# 		ldata=[]
# 		for ti in tlist:
# 			ll=ti.split()
# 			tup=(ll[0],ll[1])
# 			ldata.append(tup)
# 		data.append(ldata)

def counthashtags(thestring):
	pattern=r'(#\w+)'
	# print("out hash")
	return re.subn(pattern, '', thestring)[1]


def countupper(text):
	c=0
	for w in text.split():
		if w.isupper():
			c+=1
	# print("out upper")
	return c



def checknegation(text):
	match = re.search(r"((\b(never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)\b)|\w+n't)", text)
	if match:
		# print("out neg")
		return 1
	else:
		# print("out neg")
		return 0


def replacenegation_bigram(s):
	regex =re.compile(r"((?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)\b|\b\w+n't\b)([^.:;!?]*)([.:;!?\b])")
	return regex.sub(lambda x:x.group(1)+' '+' '.join([i+'_NEG' for i in x.group(2).split()])+x.group(3) ,s)

def replacenegation_monogram(s):
	regex =re.compile(r"((?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)\b|\b\w+n't\b)([^.:;!?]*)([.:;!?\b])")
	return regex.sub(lambda x:x.group(1)+' '+x.group(2).split()[0]+'_NEGFIRST '+' '.join([i+'_NEG' for i in x.group(2).split()[1:]])+x.group(3) ,s)


def countpos(c):
	spos=pos[c]
	postag = collections.namedtuple('Postag', ['N', 'O', 'pn','S','Z','V','L','M','A','R','inj','D','P','coo','T','X','Y','hs','at','dis','U','E','num','pun','G'])
	p = postag(spos.count('N'),spos.count('O'),spos.count('^'),spos.count('S'),spos.count('Z'),spos.count('V'),spos.count('L'),spos.count('M'),spos.count('A'),spos.count('R'),
		spos.count('!'),spos.count('D'),spos.count('P'),spos.count('&'),spos.count('T'),spos.count('X'),spos.count('Y'),spos.count('#'),spos.count('@'),spos.count('~'),
		spos.count('U'),spos.count('E'),spos.count('$'),spos.count(','),spos.count('G'))
	# print("out pos")
	return p

def lastex(sent):
	# print("out ex")
	return sent[len(sent)-1]=='!'

def lastq(sent):
	# print("out q")
	return sent[len(sent)-1]=='?'


book = pyexcel.get_book(file_name="English_Train-final.xlsx")
for sheet in book:
	text=[]
	tag=[]
	data=pyexcel.to_array(sheet.rows())

	for tweet in data:
		tx=tweet[0]
		tx=clean(tx)
		text.append(tx)
		if(tweet[1]==2):
			tag.append(tweet[2])
		tag.append(tweet[1])

	textlist=[]
	c=0
	for sent in text:
		# textlist.append([has_modal(s),has_strong(s),has_personal(s),has_long(s), has_wh(s)])
		textlist.append([has_long(sent), checknegation(sent), getnrcscore(sent),getemoscore(sent),
			counthashtags(sent), countupper(sent), lastex(sent), lastq(sent),gets140_bi(sent),gets140_uni(sent),gets140_an_bi(sent), gets140_an_uni(sent)])

		#COUNTPOS NOT ADDED

	feature=array(textlist)


	print feature

# pred= fulltrainclf.predict(feature)

# getTweets()
# for tweet in data:
# 	for line in tweet:
# 		print line[0];line[1]
# 	print '\n'

# s=raw_input()
# checknegation(s)
# print replacenegation_bigram(s)
# print replacenegation_monogram(s)
# print counthashtags(s)
# print countupper(s)

# c=0
# for t in sentences:
# 	print countpos(c)
# 	c+=1
	# print t
	# print gets140_an_bi(t)


# flist=[]
# c=0
# for sent in sentences:
# 	flist.append([has_long(sent), checknegation(sent), getnrcscore(sent),getemoscore(sent),
# 		counthashtags(sent), countupper(sent), lastex(sent), lastq(sent)],gets140_bi(sent),gets140_uni(sent),gets140_an_bi(sent), gets140_an_uni(sent))#, countpos(c)
# 	# c=c+1

# v = DictVectorizer(sparse=False)
# # X = v.fit_transform(flist)

# X=array(flist)

# print flist

# print X

# trainclf = SVC(kernel='rbf',gamma=0.5)
# trainclf.fit(X, Y)


# #CROSS VALIDATION

# X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.1, random_state=0)
# print trainclf.score(X_test, Y_test) 


