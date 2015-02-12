import os  
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
    """
    TODO: Add additional functionality - perhaps searching for all instances of searched_string within pdf_file.
    This function returns the starting place of searched_string within pdf_file. pdf_file is a string containing pdf text.  
    """     
    return pdf_file.index(searched_string)
    

searched_string = "caused"

def main():
    """
    TODO: Add command-line functionality. Discuss more design specifics before implementing.
    """
    for pdf_name in os.listdir("."):
        if pdf_name[0] == ".":
            continue
        textFromPdf = convert_pdf_to_txt(pdf_name)
        textFromPdf = textFromPdf.rstrip().replace("\\n","")
        print repr(textFromPdf)
        positionOfSearchedText = search(textFromPdf, searched_string)
        print "the index of {} in {} is {}".format(searched_string, pdf_name, positionOfSearchedText)

if __name__ == '__main__':
    main()
