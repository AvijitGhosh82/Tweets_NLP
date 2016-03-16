from pattern.en import parse
from pattern.en import pprint 
from pattern.en import parsetree

s=parsetree("To me, coming here is a way of saying goodbye. Goodbye to my friend, who meant a lot me.",chunk =True ,relations=True, lemmata=True)

# pprint(parsetree("There's so many sleeper cells, so many people just waiting",chunk =True ,relations=True, lemmata=True))


# pprint(s)
# print s

for sentence in s:
	print sentence.relations
	print sentence.pnp
	for chunk in sentence.verbs:
		print chunk.lemmata[0]


# cases: SBJ and OBJ

# or NP VP present