"""
Created on 12/5/2020

@author: sophie
"""

from openpyxl import Workbook
import InstaScrapeV9Specific

def makeSpreadsheet(urlsWKW):
    #for example:
    #row1 is name of category
    #each column a-z row 2+ is the urls in category
    workbook = Workbook()
    sheet = workbook.active
    columnASCII=65
    for sublist in urlsWKW:
        sheet[chr(columnASCII)+"1"]= sublist[0]
        #sets given column row 1 to category name
        i=1; #i is idx in sublist
        while i<len(sublist):
            sheet[str(chr(columnASCII) + str(i+1))] = sublist[i]
            i+=1
        columnASCII+=1
    workbook.save(filename="category.xlsx")


if __name__ == '__main__':
    #for reference
    listOfKWs = ['poverty','inequality','aids','hiv','conservation','hair']

    url1='www.google.com/1'
    url2='www.google.com/2'
    urlsWKW = [['poverty', url1, url2], ['inequality',url1, url2], ['aids'],
               ['hiv'], ['conservation'], ['hair']]
    makeSpreadsheet(urlsWKW)