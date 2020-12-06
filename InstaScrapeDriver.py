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

    listOfKWs = ['poverty', 'inequality', 'aids', 'hiv', 'conservation', 'hair']
    urlsWKW = InstaScrapeV9Specific.search_thru_comments(urls, listOfKWs)

    makeSpreadsheet.makeSpreadsheet(urlsWKW)