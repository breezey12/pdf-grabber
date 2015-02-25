import os  
import re
import argparse
import time
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path, pageRange=0):
    """ This converts a PDF file to a string, with an optional argument
    to specify number of pages.
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    if pageRange == 0:
        pagenos = set()
    else:
        pagenos=set(pageRange)
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
    
def clean_string(string):
    pass

           
def main():
    """loops through all the PDFs in the local directory and prints
    the first five pages starting at the second page number present
    on the table of contents.  this number is *usually* the risk disclosure,
    but not always.

    TO-DO: break this off into functions
    TO-DO: compensate for the X% that don't have risk disclosures in the second
    TOC listing.
    TO-DO: make sure it's printing the page number it's found.
    """

    files = os.listdir(".")
    for file in files:
        if file.endswith(".pdf"):
            pdf_text = convert_pdf_to_txt(file, [1,2,3,4,5,6])
#    print repr(pdf_text)
    # variations of this search should include "Exhibits
            searches = ["Exhibits and Financial", "EXHIBITS, FINANCIAL", "Exhibits, Financial"]
            for search in searches:
                first_index = pdf_text.find(search)
                if first_index != -1:
                    break
            print first_index
            titrated_loc = pdf_text[first_index:first_index+500]
            toc = re.findall("\d+", titrated_loc)
            risk_disclosure_start = int(toc[1])
            risk_disclosure_text = convert_pdf_to_txt(file, [risk_disclosure_start, risk_disclosure_start+1, risk_disclosure_start+2, risk_disclosure_start+3, risk_disclosure_start+4])
            print risk_disclosure_text 

if __name__ == '__main__':
    main()
