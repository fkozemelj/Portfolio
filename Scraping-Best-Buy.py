from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#Location of chromedriver on your local machine
driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')

#Location of the data you want to scrape
driver.get("https://www.bestbuy.ca/en-ca/search?search=microsoft+surface+3")

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product
availability=[] #List to store availability to ship

content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll(attrs={'class':'col-xs-12_198le col-sm-4_13E9O col-lg-3_ECF8k x-productListItem productLine_2N9kG'}):
    name=a.find('div', attrs={'class':'productItemName_3IZ3c'})
    price=a.find('div', attrs={'class':'productPricingContainer_3gTS3'})
    rating=a.find('div', attrs={'class':'ratingContainer_29ZF-'})
    shipping=a.find('div',attrs={'class': 'availabilityMessageSearch_23ZLw'})
    products.append(name.text)
    prices.append(price.text)
    ratings.append(rating.text)
    availability.append(shipping.text)

i = 0
while i < len(prices):
    prices[i] = (prices[i])[:8]
    i += 1

df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) #'Availability':availability}) 

df.to_csv('products.csv', index=False, encoding='utf-8')


