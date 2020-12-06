"""
Created on 12/5/2020
copied

@author: sophie
"""


# this one has new function at top which works to go through all posts. and
# list of hashtags for hackduke

from openpyxl import Workbook
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import timeit
from selenium.webdriver import Chrome

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
#not using in grey?

#to do: make a spreadhseet and add each to appropriate spreadsheet

def all_post_links(hashtag, numPosts):
    """With the input of an account page, scrape the numPost most recent posts
    urls"""
    url = "https://www.instagram.com/explore/tags/" + hashtag + "/"
    browser = webdriver.Chrome('/Users/sophie/documents/chromedriverCurrent')
    #browser = webdriver.Safari('/Users/sophie/downloads/chromedriver')
    browser.get(url)
    post = 'https://www.instagram.com/p/'

    #BELOW MAY HANDLE EXCEPTIONS
    #my_element_id = 'links'
    ignored_exceptions = (NoSuchElementException,
                          StaleElementReferenceException,)
    #links = WebDriverWait(browser, some_timeout,
                                 #ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, my_element_id)))

    post_links = []
    linkNum = 0
    while len(post_links) < numPosts:
        links=['empty link']
        #linkNum=0
        try:
            links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
            linkNum+=1
        except exceptions.StaleElementReferenceException:
            linkNum+=1
            browser.implicitly_wait(5)
            try:
                links = [a.get_attribute('href') for a in
                         browser.find_elements_by_tag_name('a')]
            except exceptions.StaleElementReferenceException:
                try:
                    links=[]
                    for a in browser.find_elements_by_tag_name('a'):
                        links.append(a.get_attribute('href'))
                except exceptions.StaleElementReferenceException:
                    print('exception print statement: post number',linkNum)
                    links.append('exception link')

        for link in links:
            #if post in link and link not in post_links:
            if link not in post_links:
                post_links.append(link)

        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        #time.sleep(10)
    else:
        return post_links[:numPosts]


def searchForEachKW(KW, script, listKWs):
    # need to change so that calls search for each KW here. so that
    # searching each link for all the hashtags, and then add link to
    # appropriatre kw spreadsheet
    if KW in script:
        print('script for one post w KW: ', script)
        shortcode = script[323:336]
        print('script[333:334]', shortcode)
        print("script.index(''shortcode'')", script.index('"shortcode"'))
        insta_link = 'https://www.instagram.com/p/' + shortcode + '/'
        # shortcode includes forward slashes around it

        i=0
        while i<len(listKWs):
            if listKWs[i][0]==KW:
                listKWs[i].append(insta_link)
            i+=1
        ##by end should have list with url added to appropriate keyword
        # subliusts
        # time.sleep(10)
    else: return


def search_thru_comments(urls, listOfKWs):
    """Take a post url and return post details"""
    browser = webdriver.Chrome('/Users/sophie/documents/chromedriverCurrent')

    listKWs = []
    for KW in listOfKWs:
        listKWs.append([KW])
    #ex: listKWs=[['poverty'], ['inequality'], ['aids'], ['hiv']]
    #list where list[something]=name of KW. append after that the urls.

    for link in urls:
        browser.get(link)

        source = browser.page_source
        data = bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('script',
                           text=lambda t: t.startswith('window._sharedData'))
        #print(script)
        script = str(script)
        #scriptSplit=script.split('shortcode')
        #print(scriptSplit)

        #pass to searchForEach which will check the indiv posts for all KWs
        # and will then add them to the appropriate spread sheet
        for KW in listOfKWs:
            searchForEachKW(KW, script, listKWs)

        #need to change so that calls search for each KW here. so that
        # searching each link for all the hashtags, and then add link to
        # appropriatre kw spreadsheet

    return listKWs

if __name__ == '__main__':

    numPosts = 6
    hashtag = 'infographic'
    #hashtag = '5056907896'


    urls=all_post_links(hashtag,numPosts)
    # return first numPosts urls from the hashtag page
    print('url list', urls)
    print('len urls gone through in hashtag',hashtag, len(urls))
    #print('time to run part 1: ', timeit(all_post_links,1))


    # goes through list of desired hashtags and calls search_thru_comments
    # for each to look through every post

    #content='@turnercarrollgallery'
    listOfKWs = ['poverty', 'inequality', 'aids', 'hiv', 'conservation', 'hair']
    for k in listOfKWs:
        print (k,listOfKWs.index(k))
    urlsWKW=search_thru_comments(urls, listOfKWs)
    # search through all the post urls  and
    # determine which have the desired kw in comments

    print('urls w KW content in comment: ',urlsWKW)
    #will print the list with list[i][0]=kw where list[i][0]=listOfKWs[i].
    # maybe best to assign them an i for easy access or print i guide?

    #will print each kw and then the number of urls
    print('len/num urls w KW content in comment: ')
    i=0
    while i<len(listOfKWs):
        print(urlsWKW[i][0],len(urlsWKW[i])-1)
        i+=1
    #print(timeit(search_thru_comments(urls, KW),1))


