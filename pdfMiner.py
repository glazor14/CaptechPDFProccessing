import pdfminer

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LTTextBoxHorizontal

# Open a PDF file.
fp = open('PGA_Tour_CapTech_SOW_Metrics_final.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF doc obj that stores document structure
document = PDFDocument(parser)
#check if document allows for text extraction
if not document.is_extractable:
	raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
#create paramaters for analysis
laparams = LAParams()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device) 
# Process each page contained in the document.
for page in PDFPage.create_pages(document):
	interpreter.process_page(page)
	layout = device.get_result()
	for elements in layout:
		if instanceof(element, LTTextBoxHorizontal):
			print(element.get_text())

