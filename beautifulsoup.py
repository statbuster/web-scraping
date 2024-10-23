"""
Web Scraping with BeautifulSoup
"""
##########################
## Crawl
##########################

# importing required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'https://www.goibibo.com/hotels/hotels-in-shimla-ct/'

# headers

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL

response = requests.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup

data = BeautifulSoup(response.content, 'html.parser')

##########################
## Parse and Transform
##########################

# Find all hotel names and prices
cards_data = data.find_all('div', attrs={'class', 'HotelCardV2styles__SRPCardWrapper-sc-6przws-0 dgWXvH'})

for card in cards_data:
    hotel_name = card.find('a')

    hotel_price = card.find('p', attrs={'class', 'HotelCardV2styles__OfferPrice-sc-6przws-18 jYyTWC'})

    print(hotel_name.text,hotel_price.text)

print('Total Number of Cards Found', len(cards_data))

##########################
## Store
##########################

scraped_data = []

for card in cards_data:

    card_details = {}

    hotel_name = card.find('a')

    hotel_price = card.find('p', attrs={'class', 'HotelCardV2styles__OfferPrice-sc-6przws-18 jYyTWC'})

    card_details['hotel_name'] = hotel_name.text
    card_details['hotel_price'] = hotel_price.text

    scraped_data.append(card_details)

dataFrame = pd.DataFrame.from_dict(scraped_data)

dataFrame.to_csv('./web-scraping/scraped_data.csv', index=False)

##########################
## Web Scraping - Scrap Images
##########################

# Find all with the image tag

images = data.find_all('img', src=True)

print('Number of Images Found:', len(images))

for image in images:
    print(image)

image_src = [x['src'] for x in images]

image = [x for x in image_src if x.endswith('.jpg')]

for index,image in enumerate(image_src):
    with open('./web-scraping/data/image_' + str(index) + '.jpg', 'wb') as f:
        f.write(requests.get(image).content)