from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # latest news scrape
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    latest_news = soup.find('div', class_='list_text')

    news_title = latest_news.find('a').text

    news_p = latest_news.find('div', class_='article_teaser_body').text

    # featured image scrape
    url2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url2)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_image_path = soup.find_all('img')[1]["src"]
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + mars_image

    # try pasting all four sections in sequence, using browser.visit to change pages.
    # then browser.quit at the end

    