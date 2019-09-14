from bs4 import BeautifulSoup
from splinter import Browser
import time 
import pandas as pd

def scrape(): 
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome",**executable_path)
    news_title, news_p = mars_news(browser)
    mars_data = {
        "news_title": news_title, 
        "news_p" : news_p,
        "feature_image" : mars_image(browser),
        "mars_weather" : mars_weather(browser),
        "mars_table" : mars_table(),
        "mars_hemispheres" : mars_hemispheres(browser)
    }

    browser.quit()
    return mars_data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    #browser = Browser('chrome')
    browser.visit(url)
    html = browser.html
    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')
    news_title= soup.find('div', class_='content_title').text
    news_p= soup.find('div', class_= 'article_teaser_body').text
    return news_title, news_p


#Image
def mars_image(browser):
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(jpl_url)
    browser.find_by_id('full_image').click()
    time.sleep(2)
    browser.click_link_by_partial_text("more info")
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img=soup.find('img',class_='main_image')['src']
    featured_image_url= base_url+img
    return featured_image_url

#Weather
def mars_weather(browser):
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    soup
    mars_weather= soup.find('ol',{"id":'stream-items-id'}).find('li').find('p').text
    return mars_weather

#Hemispheres
def mars_hemispheres(browser):
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    hemisphere_image_urls = []
    img_url = []

    for i in range(4): 
        mars_dict = {}
        btn = browser.find_by_tag("h3")[i]
        btn.click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_dict["title"] = soup.find('h2',class_="title").text
        mars_dict["hemisphere_url"] = soup.find('div', class_='downloads').find("a")['href']
        hemisphere_image_urls.append(mars_dict)
        browser.back()

    return hemisphere_image_urls

#Table
def mars_table():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    return html_table



