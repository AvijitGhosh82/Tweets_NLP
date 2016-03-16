import re
from pattern.en import parsetree
from pattern.en import tokenize


source=open('nytimes_clean.txt','r')
out=open('quote.txt','w')
out2=open('report.txt','w')
verbs=open('verbs.txt','r')
pos=open('positive-words.txt','r')
neg=open('negative-words.txt','r')
postext=open('positive_opinion.txt','w')
negtext=open('negative_opinion.txt','w')

verblist=[]
quotes=[]
reports=[]
other=[]

poslist=[]
neglist=[]
posop=[]
negop=[]


for line in verbs:
	for v in line.split("\n"):
		verblist.append(v.strip())


verblist=list(set(verblist))


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

poslist = filter(None, poslist)
neglist = filter(None, neglist)

def opinioncheck(line):
	sentences = tokenize(line)
	for s in sentences:
		tokens= tokenize(s)
		# print tokens
		for token in tokens:
			for word in token.split():
				if word in poslist:
					posop.append(line)
				if word in neglist:
					negop.append(line)




def reportcheck(line):
	s=parsetree(line,chunk =True ,relations=True, lemmata=True)
	add=False
	for sentence in s:
		add=False
		for chunk in sentence.verbs:
			v =chunk.lemmata[0]
			if v in verblist:
				reports.append(line)
				add=True
				break
	if not add:
		opinioncheck(line)


for line in source:
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
				quotes.append(line)
			else:
				reportcheck(line)
	else:
		reportcheck(line)



quotes=list(set(quotes))
reports=list(set(reports))
other=list(set(other))


for q in quotes:
	print >> out, q
for r in reports:
	print >> out2, r
for o in other:
	print >> others, o

posop=list(set(posop))
negop=list(set(negop))

# print "positive"
for p in posop:
	print >> postext, p
# print "negative"
for n in negop:
	print >> negtext, n






		# print >> out, line.split("https")[0]

source.close()
out.close()
out2.close()
verbs.close()
pos.close()
neg.close()

