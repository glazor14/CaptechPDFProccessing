import PyPDF2, sys, pprint
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def prepare_text(text_file):
	#The first step is to read text from the file
	file = open(text_file, "r")
	text = file.read()

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

	#print(keywords)
	return keywords
	

def sow_parsing_ff(text_file):
	#Prepare the text so that data can be extracted
	keywords = prepare_text(text_file)

	#Function that gets indexes of specified word in collection
	get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

	# Find the Title of the Document
	pindexes = get_indexes("Project", keywords)
	thindexes = get_indexes("This", keywords)
	a = 0
	for i in pindexes:
		if keywords[i+1] == "Title":
			break
		a = a + 1
	project_title = (keywords[pindexes[a]+2:thindexes[0]])
	project_title = ' '.join(project_title)
	print("Project Title: ", project_title)

	# Find the Client Name
	captech_indexes = get_indexes("ﬁCapTechﬂ", keywords)
	client_indexes = get_indexes("ﬁClientﬂ", keywords)

	client_name = keywords[captech_indexes[0]+2:client_indexes[0]]
	client_name = ' '.join(client_name)
	print("Client Name: ", client_name)

def SOW_Parsing_TaM(text_file):
	"""
	We have a text variable which contains all the text in pdf file.
	"""
	#Prepare the text so that data can be extracted
	keywords = prepare_text(text_file)

	#Function that gets indexes of specified word in collection
	get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

	# Find the Title of the Document
	pindexes = get_indexes("Project", keywords)
	thindexes = get_indexes("This", keywords)
	a = 0
	for i in pindexes:
		if keywords[i+1] == "Title":
			break
		a = a +1
	#print (a)
	projectTitle = (keywords[pindexes[a]+2:thindexes[0]])
	projectTitle = ' '.join(projectTitle)
	print ("Project Title: ", projectTitle)

	# Find the Client Name
	capindexes = get_indexes("ﬁCapTechﬂ", keywords)
	cindexes = get_indexes("ﬁClientﬂ", keywords)

	clientName = keywords[capindexes[0]+2:cindexes[0]]
	clientName = ' '.join(clientName)
	print("Client Name: ", clientName)

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
	clientContactInfo = ' '.join(clientContactInfo)
	print ("Client Contact Info: ", clientContactInfo)

	# Find the Captech Contact Info
	conindexes = get_indexes("captechconsulting.com", keywords)

	captechContactInfo = keywords[cpindexes[b]:conindexes[0]+1]
	captechContactInfo = ' '.join(captechContactInfo)
	print("Captech Contact Info: ", captechContactInfo)

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

	#print (a)
	servicesAndDevs = keywords[rindexes[a]:sindexes[c]-1]
	servicesAndDevs = ' '.join(servicesAndDevs)
	print ("Services and Deliverables: ", servicesAndDevs)

	# Find Dates
	bindexes = get_indexes("beginning", keywords)
	eindexes = get_indexes("end", keywords)

	a = 0
	d = 0
	for i in bindexes:
		if keywords[i+1] == "on":
			break
		a = a +1

	for i in eindexes:
		if keywords[i+1] == "ing":
			break
		d = d +1

	#print(a)
	#print(bindexes)

	begDates = keywords[bindexes[a]+2:bindexes[a]+5]
	endDates = keywords[eindexes[d]+3:eindexes[d]+6]

	print("Start Date: ", ' '.join(begDates))
	print("End Date: ", ' '.join(endDates))

	# Find Role & Responsibilities table


	# Find the Schedule

	# Find the Payment table

	rindexes = get_indexes("Role", keywords)
	tindexes = get_indexes("Total", keywords)

	#print(rindexes)
	#print(tindexes)

	a = 0

	for i in rindexes:
		if keywords[i+1] == "Rate":
			break
		a = a +1

	#print (a)
	paymentTable = ' '.join(keywords[rindexes[a]:tindexes[0]+5])

	print ("Payment Table: ", paymentTable)


