from pattern.en import tokenize

pos=open('positive-words.txt','r')
neg=open('negative-words.txt','r')
other=open('nytimes_clean.txt','r')
lines = [i for i in other if i[:-1]]


poslist=[]
neglist=[]
posop=[]
negop=[]

for line in pos:
	for v in line.split("\n"):
		if v:
			if v[0] != ';':
				poslist.append(v.strip())

for line in neg:
	for v in line.split("\n"):
		if v:
			if v[0] != ';':
				neglist.append(v.strip())

print poslist
print neglist
print lines

poslist = filter(None, poslist)
neglist = filter(None, neglist)

for line in lines:
		sentences = tokenize(line)
		for s in sentences:
			tokens= tokenize(s)
			for word in tokens:
				if word in poslist:
					posop.append(line)
				elif word in neglist:
					negop.append(line)

posop=list(set(posop))
negop=list(set(negop))

print "positive"
for p in posop:
	print p
print "negative"
for n in negop:
	print n

