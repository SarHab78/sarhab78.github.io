"""
Created on 12/5/2020

@author: sophie
"""
import makeSpreadsheet
import InstaScrapeV9Specific

if __name__ == '__main__':
    numPosts = 6
    hashtag = 'infographic'
    urls = InstaScrapeV9Specific.all_post_links(hashtag, numPosts)
    #get first mumPost urls from hashtag page

    listOfKWs = ['poverty', 'inequality', 'aids', 'hiv', 'conservation',
                 'covid', 'voting', 'racism', 'blm', 'lgbt','indigenous','lgbt']

    urlsWKW = InstaScrapeV9Specific.search_thru_comments(urls, listOfKWs)
    print(urlsWKW)
    #add the urls that contain KWs to urlsWKW

    urlsWKWDate=InstaScrapeV9Specific.listKWsDateHelper()
    print(urlsWKWDate)
    # add the dates of all urls that contain KWs to urlsWKW. indexes match
    # between urlsWKWDate and urlsWKW

    makeSpreadsheet.makeCategorySpreadsheet(urlsWKW)
    makeSpreadsheet.makeDateSpreadsheet(urlsWKWDate)
    #make spreadsheet where row 1 is category title and urls in col