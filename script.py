from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url, country):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('#form_details h4')[0].get_text().strip()
        stamp['price'] = price.replace('Our Price:', '').replace('£', '').replace(',', '').strip()
    except: 
        stamp['price'] = None
        
    try:
        stock_num = html.select('#form_details p')[1].get_text().strip()
        stock_num = stock_num.replace('Our Ref:', '').strip()
        stamp['stock_num'] = stock_num
    except:
        stamp['stock_num'] = None    
        
    stamp['currency'] = "GBP"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('#largeImage')
        for image_item in image_items:
            img = 'https://www.avionstamps.com' + image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    stamp['country'] = country 
    
    try:
        raw_text = html.select('.container h3')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.product_title_list a'):
            item_link = 'https://www.avionstamps.com' + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_url_cont = html.find('a', href=True, text="[Next]")
        if next_url_cont:
            next_url = 'https://www.avionstamps.com' + next_url_cont.get('href')
    except:
        pass        

    shuffle(list(set(items)))
    
    return items, next_url

def get_countries():

    url = 'https://www.avionstamps.com/search-by-country/' 

    countries = []

    try:
        html = get_html(url)
    except:
        return countries

    try:
        for item in html.select('.grid_2 > a'):
            country_link = 'https://www.avionstamps.com' + item.get('href')
            if country_link not in countries:
                countries.append(country_link)
    except:
        pass
    
    shuffle(countries)
    
    return countries

countries = get_countries()
for page_url in countries:
    country_parts = page_url.split('/shop/search/') 
    country = country_parts[1].replace('+', ' ').replace('/', '').strip()
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item, country)

