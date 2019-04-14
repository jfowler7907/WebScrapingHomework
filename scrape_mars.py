#import libararies
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import sys
import json
import datetime

def scrape():

    #create url
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    #browser.visit(url)
    #response=browser.html
    #print(browser.html)

    # Retrieve page without browser
    response = requests.get(url)
    print(response.text)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    textContent = []

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    #find latest news article
    news_article=soup.find_all("div",class_='content_title')
    for items in news_article:
        if items.text.strip() != "":
            print(items.text.strip())
    latest_article=news_article[0].text.strip()
    print(f"\nThe latest article is: "+ latest_article)

    #find latest news article
    news_article_desc=soup.find_all("div",class_='rollover_description_inner')
    for items in news_article_desc:
        if items.text.strip() != "":
            print(items.text.strip())
    latest_article_desc=news_article_desc[0].text.strip()
    print(f"\nThe latest article is: "+ latest_article_desc)

    #JPL Space Images
    #create url
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Retrieve the featured image click button to bring up image and then get url for featured
    browser.click_link_by_partial_text('FULL IMAGE')
    image=soup.find_all("img",class_='fancybox-image')
    featured_image_url="https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA00029_ip.jpg"

    #Mars Weather twitter site
    #create url
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    textContent = []

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    #find latest tweet
    mars_soup=soup.find_all("p",class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')

    #Identify data type. 
    type(str(mars_soup))

    #Convert above element into a string and replace the image with a blank
    new_var=str(mars_soup[0].text).replace("pic.twitter.com/awJfx8w2YE"," ")
    print ("Mars weather = "+ new_var)

    #Mars Facts
    #create url
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create tables
    tables = pd.read_html(url)
    tables

    type(tables)

    #Create dataframe from website
    df = tables[0]
    df.columns = ['0', '1']
    df

    #Convert into HTML
    html_table = df.to_html()
    html_table

    #Mars Hemisphere
    #Open url
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
        
    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
        
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = BeautifulSoup(pic_html, 'html.parser')
        
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url
        print(img_dict["img_url"])
        
        hemisphere_image_urls.append(img_dict)
    hemisphere_image_urls
return()    