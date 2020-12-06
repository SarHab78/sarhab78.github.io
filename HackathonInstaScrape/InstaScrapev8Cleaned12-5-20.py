"""
Created on 6/2/2020

@author: sophie
"""


#this one has new function at top which works to go through all posts


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


def search_thru_comments(urls, KW):
    """Take a post url and return post details"""
    browser = webdriver.Chrome('/Users/sophie/documents/chromedriverCurrent')
    linksWitKW = []
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
        print(KW in script)
        if KW in script:
            print('script for one post w KW: ', script)
            shortcode=script[323:336]
            print('script[333:334]', shortcode)
            print("script.index(''shortcode'')", script.index('"shortcode"'))
            insta_link = 'https://www.instagram.com/p/'+shortcode + '/'
            #shortcode includes forward slashes around it
            linksWitKW.append(insta_link)
            #time.sleep(10)

    return linksWitKW

if __name__ == '__main__':
    numPosts = 10
    hashtag = 'createartforearth'
    #hashtag = '5056907896'

    urls=all_post_links(hashtag,numPosts)
    # look through the first numPosts of the hashtag page
    print('url list', urls)
    print('len urls', len(urls))
    #print('time to run part 1: ', timeit(all_post_links,1))

    content='@turnercarrollgallery'
    urlsWKW=search_thru_comments(urls, content)
    # search through all the post urls  and
    # determine which have the desired kw in comments
    print('urls w KW content in comment: ',urlsWKW)
    print('len/num urls w KW content in comment: ', len(urlsWKW))
    #print(timeit(search_thru_comments(urls, KW),1))

