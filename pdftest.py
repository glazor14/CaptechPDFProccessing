import PyPDF2, sys, pprint
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

name = ''.join(sys.argv[1:])

#pdfFileObj = open('PGA_Tour_CapTech_SOW_Metrics_final.pdf', 'rb')
pdfFileObj = open(name, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#print(pdfReader.numPages)

#pageObj = pdfReader.getPage(0)

#print(pageObj.extractText())
num_pages = pdfReader.numPages
count = 0
text = ""

while count < num_pages:
	pageObj = pdfReader.getPage(count)
	count += 1
	text += pageObj.extractText()

# PyPDF2 Cannot read scanned files!!

"""
We have a text variable which contains all the text in pdf file.
"""

#The word_tokenize() function will break our text phrases into #individual words
tokens = word_tokenize(text)

#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',','.']

stop_words = stopwords.words('english')

#We create a list comprehension which only returns a list of words 
#that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word 
in stop_words and not word in punctuations]

#index = keywords.index('Engineer')

get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

indexes = get_indexes("Senior", keywords)

#np.rfind(keywords, )

print (keywords[indexes[2]:indexes[2]+8])

#print (keywords[index:index+3])

pp = pprint.PrettyPrinter(indent=4)

#pp.pprint(keywords)


#print( minutesFirstPage)

#pdfWatermarkReader = PyPDF2.PdfFileReader