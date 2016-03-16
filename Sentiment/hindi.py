# -*- coding: utf-8 -*-

# The path to the local git repo for Indic NLP library
INDIC_NLP_LIB_HOME="/Users/Avijit/Documents/nlp_lib"
# The path to the local git repo for Indic NLP Resources
INDIC_NLP_RESOURCES="/Users/Avijit/Documents/nlp_res"

from indicnlp import common
common.set_resources_path(INDIC_NLP_RESOURCES)

from indicnlp import loader
loader.load()


from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

input_text=u"\u0958 \u0915\u093c"
remove_nuktas=False
factory=IndicNormalizerFactory()
normalizer=factory.get_normalizer("hi",remove_nuktas)
output_text=normalizer.normalize(input_text)

print output_text
print 'Length before normalization: {}'.format(len(input_text))
print 'Length after normalization: {}'.format(len(output_text))