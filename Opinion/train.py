from pandas import read_csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import HTMLParser
html_parser = HTMLParser.HTMLParser()
from nltk.classify import SklearnClassifier
from sklearn.svm import SVC
import re
from collections import Counter

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

def clean(text):
	text=html_parser.unescape(text)
	# text.decode("utf8").encode('ascii','ignore')
	#convert to unicode
	text = unicode(text, 'utf-8')

	#encode it with string escape
	text = text.encode('unicode_escape');
	# text=re.sub(r"http\S+", "", text)
	# text=" ".join(re.findall('[A-Z][^A-Z]*', text))
	tl=tknzr.tokenize(text)
	newtext=""
	for t in tl:
		newtext+=t+" "
	return newtext

# def get_word_features(wordlist):
#     wordlist = nltk.FreqDist(wordlist)
#     word_features = wordlist.keys()
#     return word_features

# def get_words_in_tweets(tweets):
#     all_words = []
#     for (words, sentiment) in tweets:
#       all_words.extend(words)
#     return all_words

# def extract_features(document):
#     document_words = set(document)
#     features = {}
#     for word in word_features:
#         features['contains(%s)' % word] = (word in document_words)
#     return features



def traindict(tweets):
	training_set=[]
	for text,tag in tweets:
		td=dict(Counter(text))
		training_set.append((td,tag))
	return training_set

df = read_csv('labelledtweets_2.csv')
# df.columns = ['tag', 'sno','date','sub','user','text']
# df.to_csv('labelledtweets_2.csv')
train=[]

for i,r in df.iterrows():
	tx=clean(r['text'])
	if r['tag']==2:
		train.append((tx,"obj"))	
	# elif r['tag']==0:
	#  	train.append((tx,"neg"))	
	else:
		train.append((tx,"subj"))	





tweets = []
stop_words = set(stopwords.words('english'))

for (words, sentiment) in train:
	words_filtered = [e.lower() for e in words.split() if e not in stop_words]
	tweets.append((words_filtered, sentiment))

# print tweets
# word_features = get_word_features(get_words_in_tweets(tweets))
# training_set = nltk.classify.apply_features(extract_features, tweets)

training_set=traindict(tweets)
print training_set

# classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier =  SklearnClassifier(SVC(), sparse=False).train(training_set)

tweetd = 'I have cows :('
print classifier.classify(dict(Counter(clean(tweetd.lower()))))



# tweetd = 'Obama is boring :('
# print classifier.classify(extract_features(tweetd.lower().split()))
