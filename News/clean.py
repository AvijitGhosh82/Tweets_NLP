import re

source=open('nytimes_raw.txt','r')
out=open('nytimes_clean.txt','w')

for line in source:
	# re.sub('RT @\w+: ', '',line)
	match=re.search(r'RT @\w+:',line)
	if match:
		# print match.group()
		line=re.sub(r'RT @\w+: ','',line)
		# print line
	if line !='\n':
		line=line[:-14]
		print >> out, line.split("http")[0]
# 'RT @[\w.-]+:'
source.close()
out.close()

