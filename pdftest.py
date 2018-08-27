import PyPDF2, sys, pprint, os
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import MWETokenizer
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from unidecode import unidecode

def prepare_text(text_file):
	# The first step is to read text from the file
	file = open(text_file, "r")
	text = file.read()
	text = unidecode(text)

	# The word_tokenize() function will break our text phrases into #individual words
	tokens = word_tokenize(text)

	# Check if text file is empty
	if not tokens:
		print("ERROR: PDF Scraping Failed")
		os.remove(text_file)
		return None

	# We'll create a new list which contains punctuation we wish to clean
	punctuations = ['(',')',';',':','[',']',',','.', '\"', '\'', '``', "''", '•']

	

	#stop_words = stopwords.words('english')

	# We create a list comprehension which only returns a list of words 
	# that are NOT IN stop_words and NOT IN punctuations.
	# keywords = [word for word in tokens if not word 
	# in stop_words and not word in punctuations]

	keywords = [word for word in tokens if not word in punctuations]

	return keywords
	

def sow_parsing_ff(text_file):
	print("\nNEW SOW")
	print(text_file)

	# Prepare the text so that data can be extracted
	keywords = prepare_text(text_file)

	# Check if scraping failed
	if keywords == None:
		return

	# Function that gets indexes of specified word in collection
	get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x.lower() == y.lower()]

	# Find the Title of the Document
	pindexes = get_indexes("project", keywords)
	thindexes = get_indexes("this", keywords)
	a = 0
	for i in pindexes:
		if keywords[i+1] == "Title":
			break
		a = a + 1
	project_title = (keywords[pindexes[a]+2:thindexes[0]])
	project_title = ' '.join(project_title)
	print("Project Title: ", project_title)

	# Find the SOW number
	num_indexes = get_indexes("number", keywords)
	sow_number = -1
	if (keywords[num_indexes[1]+1] == '#'):
		sow_number = keywords[num_indexes[1]+2]
	else:
		sow_number = keywords[num_indexes[1]+1]
	print("SOW Number: ", sow_number)

	# Find the effective date
	eff_indexes = get_indexes("effective", keywords)
	effective_date = keywords[eff_indexes[0]+1:eff_indexes[0]+4]
	effective_date = ' '.join(effective_date)
	print("Effective Date: ", effective_date)

	# Find the Client Name
	captech_indexes = get_indexes("captech", keywords)

	a = 0
	for i in captech_indexes:
		if keywords[i+1:i+4] == ["Ventures", "Inc.", "CapTech"]:
			a = i + 5
			break
	client_name = []
	while keywords[a] != "Client":
		client_name.append(keywords[a])
		a = a + 1
	client_name = ' '.join(client_name)
	if len(client_name) > 50:
		client_name = "ERROR: Could not read"
	print("Client Name: ", client_name)

	# Find the fixed fee
	fee_indexes = get_indexes("$", keywords)
	fixed_fee = keywords[fee_indexes[0]+1]
	print("Fixed Fee: ", fixed_fee)

	#pp = pprint.PrettyPrinter(indent=4)
	#if project_title == "Barings SEO":
	#	pp.pprint(keywords)


def SOW_Parsing_TaM(text_file):
	print("NEW SOW")

	"""
	We have a text variable which contains all the text in pdf file.
	"""
	#Prepare the text so that data can be extracted
	keywords = prepare_text(text_file)

	#Function that gets indexes of specified word in collection
	get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]

	pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(keywords)
	# Find the Title of the Document
	pindexes = get_indexes("Project", keywords)
	thindexes = get_indexes("This", keywords)
	a = 0
	for i in pindexes:
		if keywords[i+1] == "Title":
			break
		a = a +1
	projectTitle = (keywords[pindexes[a]+2:thindexes[0]])
	projectTitle = ' '.join(projectTitle)
	print ("Project Title: ", projectTitle)

	# Find the SOW number
	num_indexes = get_indexes("number", keywords)
	sow_number = -1
	if (keywords[num_indexes[1]+1] == '#'):
		sow_number = keywords[num_indexes[1]+2]
	else:
		sow_number = keywords[num_indexes[1]+1]
	print("SOW Number: ", sow_number)

	# Find the Client Name
	capindexes = get_indexes("CapTech", keywords)
	cindexes = get_indexes("Client", keywords)

	#print (a)
	#print (capindexes)
	#print (cindexes)

	clientName = keywords[capindexes[0]+7:cindexes[0]-1]
	clientName = ' '.join(clientName)
	print("Client Name: ", clientName)

	# Find the Client Contact Info
	cciIndexes = get_indexes("Client", keywords)
	cpindexes = get_indexes("Inc.", keywords)
	a = 0
	for i in cciIndexes:
		if keywords[i+1] == "Contact" and keywords[i+2] == "Information":
			break
		a = a + 1

	b = 0
	for i in cpindexes:
		if keywords[i+1] == "Keith" and keywords[i+2] == "Smith":
			break
		b = b + 1

	#print("a", a, "b", b)
	#print(cciIndexes)
	#print(cpindexes)
	clientContactInfo = keywords[cciIndexes[a]+6:cpindexes[b]-2]
	clientContactInfo = ' '.join(clientContactInfo)
	print ("Client Contact Info: ", clientContactInfo)

	# Find the Captech Contact Info
	conindexes = get_indexes("captechconsulting.com", keywords)

	captechContactInfo = keywords[cpindexes[b]+1:conindexes[0]+1]
	captechContactInfo = ' '.join(captechContactInfo)
	print("Captech Contact Info: ", captechContactInfo)

	# Description of Services & Deliverables
	rindexes = get_indexes("Role", keywords)

	sindexes = get_indexes("Schedule", keywords)

	a = 0
	c = 0

	#print (rindexes)
	#print (sindexes)

	for i in rindexes:
		if keywords[i+3] == "Responsibilities" or keywords[i+2] == "Responsibilities" or keywords[i+4] == "Responsibilities":
			break
		a = a +1

	for i in sindexes:
		if keywords[i+1] == "III":
			break
		c = c +1

	#print ("a", a, "c", c)
	servicesAndDevs = keywords[rindexes[a]:sindexes[c]]
	servicesAndDevs = ' '.join(servicesAndDevs)
	print ("Services and Deliverables: ", servicesAndDevs)

	# Find Dates
	bindexes = get_indexes("beginning", keywords)
	eindexes = get_indexes("ending", keywords)

	a = 0
	d = 0
	for i in bindexes:
		if keywords[i+1] == "on":
			break
		a = a +1

	for i in eindexes:
		if keywords[i+1] == "on":
			break
		d = d +1

	#print(a)
	#print(bindexes)

	begDates = keywords[bindexes[a]+2:bindexes[a]+5]
	endDates = keywords[eindexes[d]+2:eindexes[d]+5]

	print("Start Date: ", ' '.join(begDates))
	print("End Date: ", ' '.join(endDates))

	# Find Role & Responsibilities table


	# Find the Schedule

	# Find the Payment table

	rindexes = get_indexes("Payment", keywords)
	tindexes = get_indexes("Rate", keywords)
	eindexes = get_indexes("Estimated", keywords)
	totindexes = get_indexes("Total", keywords)

	#print(rindexes)
	#print(tindexes)

	a = 0
	b = 0
	h = 0
	c = 0
	f = 0

	for i in rindexes:
		if keywords[i+1] == "Role":
			break
		a = a +1

	for i in tindexes:
		if keywords[i+1] == '$':
			break
		b = b + 1

	for i in eindexes:
		if keywords[i+1] == 'Hours':
			break
		h = h + 1

	for i in eindexes:
		if keywords[i+1] == 'Cost':
			break
		c = c + 1

	for i in totindexes:
		if keywords[i+2] == '$':
			break
		f = f + 1

	#print (a)
	role = keywords[rindexes[a] + 2:tindexes[b]]
	eHours = keywords[eindexes[h] + 2:eindexes[c]]
	eCost = keywords[eindexes[c]+ 2:totindexes[f]]
	total = keywords[totindexes[f]+1: totindexes[f]+4]

	paymentTable = ' '.join(keywords[rindexes[a]:tindexes[0]+5])

	print("Role: ", ' '.join(role))
	print("Estimated Hours: ", ' '.join(eHours))
	print("Estimated Cost: ", ' '.join(eCost))
	print("Total: ", ' '.join(total))

	#print ("Payment Table: ", paymentTable)


