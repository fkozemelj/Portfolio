#!/usr/bin/env python
# coding: utf-8

# ## Importing libraries

# In[1]:


import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver

from time import sleep
from random import randint


# In[2]:


i = input('Enter a item you want to compare prices: ').split(' ')


# In[3]:


product = []
price = []
store = []


# ## MEC

# In[4]:


url = 'https://www.mec.ca/en/search?org_text=' + (i[0] + '%20' + i[1] + '&text=' + i[0] + '%20' + i[1] if len(i)>1 else i[0] + '&text=' + i[0])


# In[5]:


driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver.exe')

driver.get(url)

content = driver.page_source

soup = BeautifulSoup(content)


# In[6]:


gear_div = soup.findAll(attrs={'class':'flexigrid__tile js-plp-with-takeovers__tile qa-plp-with-takeovers__tile'})


# In[7]:


for container in gear_div:

    name = container.p.a.text
    product.append(name)
    
    prices = container.find('span', class_='qa-single-price').text
    price.append(prices)
    
    store.append('MEC')


# ## Atmosphere

# In[8]:


url = 'https://www.atmosphere.ca/search.html?q=' + (i[0] + '%20' + i[1] if len(i)>1 else i[0]) + ';page=1'


# In[9]:


driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver.exe')

driver.get(url)

content = driver.page_source

soup = BeautifulSoup(content)


# In[10]:


gear_div = soup.findAll(attrs={'class':'product-grid__list-item product-grid__list-item_state_comparable'})


# In[12]:


for container in gear_div:
    
    name = container.find('span', class_='product-title-text').text
    product.append(name)
    
    prices = container.find('span', class_='product-price-text').text if container.find('span', class_='product-price-text') else container.find('span', class_='product-price__now-price-text').text
    price.append(prices)
    
    store.append('Atmosphere')


# ## The Last Hunt

# In[13]:


url = 'https://www.thelasthunt.com/search/?q=' + (i[0] + '%20' +i[1] if len(i)>1 else i[0])


# In[14]:


driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver.exe')

driver.get(url)

content = driver.page_source

soup = BeautifulSoup(content)


# In[15]:


gear_div = soup.findAll(attrs={'itemprop':'itemListElement'})


# In[16]:


for container in gear_div:
    
    brand = container.find('a', class_='ss-product__info__anchor ss-product__info__manufacturer').text
    name = container.find('a', class_='ss-product__info__anchor ss-product__info__name').text
    name = name.split('\n', 1)[0]
    product.append(brand + ' ' + name)
    
    prices = container.find('span', class_="ss-product__price--special").text if container.find('span', class_="ss-product__price--special") else container.find('span', class_="ss-product__price ss-product__price--old").text
    prices = prices.split()[1]
    price.append(prices)
    
    store.append('The Last Hunt')


# ## Valhalla Pure Outfitters 

# In[17]:


url = 'https://vpo.ca/search?searchterm=' + i[0] + ('+' + i[1] if len(i)>1 else '')


# In[18]:


driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver.exe')

driver.get(url)

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')


# In[19]:


gear_div = soup.findAll(attrs={'class':'col-md-3 col-sm-6 col-xs-12 productBox ng-scope'})


# In[20]:


for container in gear_div:
    
    brand = container.find('h5', class_='ng-binding').text
    name = container.find('a', class_='ng-binding').text
    product.append(brand + ' ' + name)
    
    prices = container.find('p', class_="ThumbPrice ng-binding").text
    price.append(prices)
    
    store.append('VPO')


# ## Storing values

# In[21]:


df = pd.DataFrame({'Product Name':product,'Price':price,'Store':store}) 


# In[23]:


df.to_csv('products.csv', index=False, encoding='utf-8')

