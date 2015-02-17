import os  
import re
import argparse
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
    pdf_file = pdf_file.lower()
    searched_string = searched_string.lower()     
    # make an iterator containing matchObjects from the search term
    matches = re.finditer(searched_string, pdf_file)
    # create a list of the index of the start of each match
    matchIndices = []
    for match in matches:
        matchIndices.append(match.start())
    return matchIndices 


def main():
    parser = argparse.ArgumentParser(description="take a search term and search for it in PDFs")
    parser.add_argument("search_term", type=str, help="the search term -- can only be one word, no quotes required")
    args = parser.parse_args()
    searched_string = args.search_term
    for filename in os.listdir("."):
        if filename.endswith('.pdf'):
            textFromPdf = convert_pdf_to_txt(filename)
            textFromPdf = textFromPdf.rstrip().replace("\\n","")
            # print repr(textFromPdf) # prints all characters, including hidden ones
            positionsOfSearchedText = search(textFromPdf, searched_string)
            if len(positionsOfSearchedText) == 0:
                print "Nothing was found in {}".format(filename)
            else:
                for position in positionsOfSearchedText:
                    print "the index of '{}' in {} is {}".format(searched_string, filename, position)
        else:
            continue

if __name__ == '__main__':
    main()
