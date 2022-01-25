#!/usr/bin/env python
# coding: utf-8

# In[56]:


import numpy as np 
import pandas as pd 
import sqlite3
import matplotlib.pyplot as plt
import matplotlib


# In[2]:


path = "C:/Users/fkoze/Desktop/Data_Science/Projects/All/SF_Bike_Data/"
database = path + 'database.sqlite'


# In[3]:


conn = sqlite3.connect(database)

read = pd.read_sql

tables = read("""SELECT *
                    FROM sqlite_master
                    WHERE type='table'
                    ;""", conn)
tables


# In[4]:


#Trips with longest duration

read("""SELECT *
            FROM trip
            ORDER BY duration DESC
            LIMIT 10
            ;""", conn)


# In[5]:


#Amount of trips that are longer than 24h

read("""SELECT count(*)
            AS \'Long Trips\'
        FROM trip  
        WHERE duration >= 60*60*24
        ;""", conn)


# In[6]:


#Proportion of unregistered users

df = read("""SELECT subscription_type, 
                count(*) AS count
            FROM trip
            GROUP BY subscription_type
            ;""",conn)


labels = ['Casual', 'Subscriber']
sizes = df['count']
colors = ['lightblue', 'lightgreen']
explode = (0.2, 0) 


plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140, )
plt.title('Subscribed vs Unsubscribed Riders')
plt.axis('equal')

plt.show()


# In[7]:


#Average duration of the trip

read("""SELECT subscription_type,
            AVG(duration)/60 AS 'Average Duration'
        FROM trip        
        GROUP BY subscription_type        
        ;""", conn)


# In[8]:


#Most popular stations

read("""SELECT station.name AS Station, 
            count(*) AS Count
        FROM station        
        INNER JOIN trip
        ON station.id = trip.start_station_id
        GROUP BY station.name        
        ORDER BY count DESC
        LIMIT 7        
        ;""", conn)


# In[9]:


# Stations with most empty readings (meaning, no bikes left to rent)

read("""SELECT station.name AS Station, 
            count(*) AS 'Total Empty Readings'
        FROM station        
        INNER JOIN status
        ON status.station_id=station.id
        WHERE status.bikes_available=0
        GROUP BY station.name
        ORDER BY count(*) DESC
        LIMIT 10        
        ;""",conn)


# In[10]:


# Distribution of available bikes for all stations

df = read("""SELECT bikes_available AS 'Bikes Available'
            FROM status
            ;""",conn)

df['Bikes Available'].plot.hist(bins=27, title='Bikes Available (All Stations)', ec='black', alpha=0.5)


# In[11]:


# Most popular routes

read("""SELECT start_station_name, 
            end_station_name, 
            COUNT(*) AS Count
        FROM trip
        GROUP BY start_station_name, end_station_name
        ORDER BY Count DESC
        LIMIT 10
        ;""",conn)


# In[38]:


df = read("""SELECT start_date FROM trip;""", conn)


# In[39]:


df.start_date = pd.to_datetime(df.start_date, format='%m/%d/%Y %H:%M')


# In[40]:


df['date'] = df.start_date.dt.date


# In[41]:


dates = {}
for d in df.date:
    if d not in dates:
        dates[d] = 1
    else:
        dates[d] += 1


# In[42]:


df2 = pd.DataFrame.from_dict(dates, orient = "index")
df2['date'] = df2.index
df2['trips'] = df2.loc[:,0]


# In[46]:


df2.drop(labels=0, axis = 1)


# In[57]:


dates = matplotlib.dates.date2num(df2['date'])


# In[70]:


matplotlib.pyplot.plot_date(dates, df2['trips'], color = 'red', figsize=(12,7))


# In[ ]:




