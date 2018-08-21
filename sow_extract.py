import sys, glob
import pdf2txt
from pdftest import *

def scrape_and_parse(pdf_file_name, text_file_name):
    pdf2txt.main([pdf_file_name, "-o", text_file_name])
    sow_parsing_ff(text_file_name)
    #SOW_Parsing_TaM(text_file_name)

def main(args=None):
    import argparse
    P = argparse.ArgumentParser(description=__doc__)
    P.add_argument("-I", "--input-dir", type=str, default="/", help="Input (pdf) directory")
    P.add_argument("-O", "--output-dir", type=str, default="/", help="Output (text) directory")
    A = P.parse_args(args=args)

    input_path = A.input_dir + "*.pdf"
    output_path = A.output_dir
    for pdf_file in glob.glob(input_path):
        text_file = output_path + pdf_file[len(output_path)-1:-3] + "txt"
        scrape_and_parse(pdf_file, text_file)

if __name__ == '__main__': sys.exit(main())