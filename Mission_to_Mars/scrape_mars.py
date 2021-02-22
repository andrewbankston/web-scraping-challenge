from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

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
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + mars_image_path

    # try pasting all four sections in sequence, using browser.visit to change pages.
    # then browser.quit at the end

    # mars facts table scrape
    url3 = "https://space-facts.com/mars/"

    tables = pd.read_html(url3)
    mars_df = tables[0]
    mars_df.columns = ['', 'Mars']
    mars_df.set_index('', inplace=True)
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    mars_df.to_html('table.html')

    # mars images scrape
    hemisphere_img_urls = []

    xpaths = ['//*[@id="product-section"]/div[2]/div[1]/div/a/h3', '//*[@id="product-section"]/div[2]/div[2]/div/a/h3', '//*[@id="product-section"]/div[2]/div[3]/div/a/h3', '//*[@id="product-section"]/div[2]/div[4]/div/a/h3']

    for xpath in xpaths:
    
        img_dict = {}

        url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url4)

        time.sleep(1)
    
        results = browser.find_by_xpath(xpath)
        img = results
        img.click()

        html = browser.html
        soup = bs(html, 'html.parser')

        img_title = soup.find("h2", class_="title").text

        img_section = soup.find_all("dl")
        img_url = img_section[0].find('a')['href']
        
        img_dict['title'] = img_title
        img_dict['img_url'] = img_url
        
        hemisphere_img_urls.append(img_dict)
        
    mars_data = {
        "latest_news_title": news_title,
        "latest_news_text": news_p,
        "jpl_image": featured_image_url,
        "html_table": html_table,
        "mars_images": hemisphere_img_urls
    }

    browser.quit()

    return mars_data
    