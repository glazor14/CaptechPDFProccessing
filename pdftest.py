import PyPDF2, sys, pprint
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def SOW_Parsing_TaM(keywords):
	get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

	# Find the Title of the Document
	pindexes = get_indexes("Project", keywords)
	thindexes = get_indexes("This", keywords)
	a = 0
	for i in pindexes:
		if keywords[i+1] == "Title":
			break
		a = a +1
	print (a)
	projectTitle = (keywords[pindexes[a]+2:thindexes[0]])
	print (projectTitle)

	# Find the Client Name
	capindexes = get_indexes("ﬁCapTechﬂ", keywords)
	cindexes = get_indexes("ﬁClientﬂ", keywords)

	clientName = keywords[capindexes[0]+2:cindexes[0]]
	print(clientName)

	# Find the Client Contact Info
	cciIndexes = get_indexes("Client", keywords)
	cpindexes = get_indexes("CapTech", keywords)
	a = 0
	for i in cciIndexes:
		if keywords[i+1] == "Contact" and keywords[i+2] == "Information":
			break
		a = a + 1

	b = 0
	for i in cpindexes:
		if keywords[i+1] == "Contact" and keywords[i+2] == "Information":
			break
		b = b + 1

	clientContactInfo = keywords[cciIndexes[a] + 3:cpindexes[b]]

	print (clientContactInfo)

	# Find the Captech Contact Info
	conindexes = get_indexes("captechconsulting.com", keywords)

	captechContactInfo = keywords[cpindexes[b]:conindexes[0]+1]

	print(captechContactInfo)

	# Description of Services & Deliverables
	rindexes = get_indexes("Role", keywords)

	sindexes = get_indexes("Schedule", keywords)

	a = 0
	c = 0

	for i in rindexes:
		if keywords[i+1] == "Responsibilities":
			break
		a = a +1

	for i in sindexes:
		if keywords[i-1] == "III":
			break
		c = c +1

	print (a)

	print ((keywords[rindexes[a]:sindexes[c]-1]))

	# Find Dates


	# Find Role & Resonsibilities table

	# Find the Schedule

	# Find the Payment table

	rindexes = get_indexes("Role", keywords)
	tindexes = get_indexes("Total", keywords)

	print(rindexes)
	print(tindexes)

	a = 0

	for i in rindexes:
		if keywords[i+1] == "Rate":
			break
		a = a +1

	print (a)

	print ((keywords[rindexes[a]:tindexes[0]+5]))


name = ''.join(sys.argv[1:])

#pdfFileObj = open('PGA_Tour_CapTech_SOW_Metrics_final.pdf', 'rb')
pdfFileObj = open(name, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pp = pprint.PrettyPrinter(indent=4)

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

#pp.pprint(text)

"""
We have a text variable which contains all the text in pdf file.
"""

#The word_tokenize() function will break our text phrases into #individual words
tokens = word_tokenize(text)

#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',','.']

#stop_words = stopwords.words('english')

#We create a list comprehension which only returns a list of words 
#that are NOT IN stop_words and NOT IN punctuations.
#keywords = [word for word in tokens if not word 
#in stop_words and not word in punctuations]

keywords = [word for word in tokens if not word in punctuations]

#retoke = MWETokenizer(keywords)

pp.pprint(keywords)

SOW_Parsing_TaM(keywords)

#index = keywords.index('Engineer')

#get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

#rindexes = get_indexes("Role", keywords)

#tindexes = get_indexes("Total", keywords)

#print(rindexes)

#print(tindexes)

#a = 0
"""
for i in rindexes:
	if keywords[i+1] == "Rate":
		break
	a = a +1

print (a)

print ((keywords[rindexes[a]:tindexes[0]+5]))
"""
#print (keywords[index:index+3])
#pp.pprint(keywords)

#pp.pprint(retoke.split())

#print( minutesFirstPage)

#pdfWatermarkReader = PyPDF2.PdfFileReader

