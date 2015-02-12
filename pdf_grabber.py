import os  
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import os  
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path):
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
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def search(pdf_file, searched_string):
    """This function returns the starting place of searched_string within pdf_file. pdf_file is a string containing pdf text.  
    """     
    # make an iterator containing matchObjects from the search term
    matches = re.finditer(searched_string, pdf_file)
    # create a list of the index of the start of each match
    matchIndices = []
    for match in matches:
        matchIndices.append(match.start())
    return matchIndices 

searched_string = "the"

def main():
    """
    TODO: Add command-line functionality. Discuss more design specifics before implementing.
    """
    for pdf_name in os.listdir("."):
        if pdf_name.endswith('.pdf'):
            textFromPdf = convert_pdf_to_txt(pdf_name)
            textFromPdf = textFromPdf.rstrip().replace("\\n","")
            print repr(textFromPdf)
            positionsOfSearchedText = search(textFromPdf, searched_string)
            for position in positionsOfSearchedText:
                print "the index of '{}' in {} is {}".format(searched_string, pdf_name, position)
        else:
            continue

if __name__ == '__main__':
    main()

def convert_pdf_to_txt(path):
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
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def search(pdf_file, searched_string):
    """
    TODO: Add additional functionality - perhaps searching for all instances of searched_string within pdf_file.
    This function returns the starting place of searched_string within pdf_file. pdf_file is a string containing pdf text.  
    """     
    # make an iterator containing matchObjects from the search term
    matches = re.finditer(searched_string, pdf_file)
    # create a list of the index of the start of each match
    matchIndices = []
    for match in matches:
        matchIndices.append(match.start())
    return matchIndices 

searched_string = "the"

def main():
    """
    TODO: Add command-line functionality. Discuss more design specifics before implementing.
    """
    for pdf_name in os.listdir("."):
        if pdf_name.endswith('.pdf'):
            textFromPdf = convert_pdf_to_txt(pdf_name)
            textFromPdf = textFromPdf.rstrip().replace("\\n","")
            print repr(textFromPdf)
            positionsOfSearchedText = search(textFromPdf, searched_string)
            for position in positionsOfSearchedText:
                print "the index of '{}' in {} is {}".format(searched_string, pdf_name, position)
        else:
            continue

if __name__ == '__main__':
    main()
