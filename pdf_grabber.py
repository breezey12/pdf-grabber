import os  
import re
import argparse
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path):
    fp = file(path, 'rb')
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    resourceManager = PDFResourceManager()
    string_io = StringIO()
    codec = 'utf-8'
    layout_parameters = LAParams()
    device = TextConverter(resourceManager, string_io, codec=codec, laparams=layout_parameters)
    interpreter = PDFPageInterpreter(resourceManager, device)
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = string_io.getvalue()
    string_io.close()
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


def main():
    # make an ArgumentParser object
    parser = argparse.ArgumentParser(description="take a search term and search for it in PDFs")
    # add a positional argument for a search term
    parser.add_argument("search_term", type=str, help="the search term -- can only be one word, no quotes required")
    # parse the arguments and store them in a variable
    args = parser.parse_args()
    # assign variable "searched_string" to the "search_term" argument
    searched_string = args.search_term
    # loop through all PDFs in the current directory
    for filename in os.listdir("."):
        if filename.endswith('.pdf'):
            textFromPdf = convert_pdf_to_txt(filename)
            # this isn't currently working, but this is an attempt to strip some weird double-escaped line breaks out
            textFromPdf = textFromPdf.rstrip().replace("\\n","")
            # print repr(textFromPdf) # prints all characters, including hidden ones
            # get a list of the indices of every occurrence of the search term
            positionsOfSearchedText = search(textFromPdf, searched_string)
            # display the locations of the search term in a readable format
            for position in positionsOfSearchedText:
                print "the index of '{}' in {} is {}".format(searched_string, filename, position)
        # don't search any files that don't end with ".pdf"
        else:
            continue

if __name__ == '__main__':
    main()
