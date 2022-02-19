#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier


# In[2]:


df = pd.read_csv("ClaimData.csv")


# In[3]:


df.head(10)


# In[4]:


df['ClaimId'].nunique()


# In[5]:


df['LineItemID'].nunique()


# In[6]:


df['Condition'].nunique()


# In[7]:


df['DiagnosisOne'].nunique()


# In[8]:


df['DiagnosisOne'].isnull().sum()


# In[9]:


df['DiagnosisTwo'].isnull().sum()


# In[10]:


fig = plt.figure(figsize=(10,6))
df.groupby('Condition').DiagnosisOne.count().plot.bar(ylim=0)
plt.show()


# In[11]:


col = ['ItemDescription', 'DiagnosisOne', 'Condition']
df_id = df[col]
df_id = df_id[pd.notnull(df_id['DiagnosisOne'])]


# In[12]:


df_id['Condition_ID'] = df_id['Condition'].factorize()[0]


# In[13]:


df_id


# In[14]:


desc = df_id['DiagnosisOne'] +' ' + df_id['ItemDescription']


# In[15]:


X_train, X_test, y_train, y_test = train_test_split(desc, df_id['Condition'], test_size= 0.20, random_state = 5)

count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(X_train)

X_train_tfidf = TfidfTransformer().fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)


# In[16]:


X_test_dtm = count_vect.transform(X_test)


# In[17]:


y_pred_class = clf.predict(X_test_dtm)


# In[18]:


print(metrics.classification_report(y_test, y_pred_class))


# In[19]:


X_train, X_test, y_train, y_test = train_test_split(desc, df_id['Condition'], test_size= 0.2, random_state = 5)

count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(X_train)

X_train_tfidf = TfidfTransformer().fit_transform(X_train_counts)


# In[20]:


rnd = RandomForestClassifier().fit(X_train_tfidf, y_train)


# In[21]:


X_test_dtm = count_vect.transform(X_test)

y_pred_class = rnd.predict(X_test_dtm)

print(metrics.classification_report(y_test, y_pred_class))


# In[22]:


df2 = pd.read_csv('Holdout.csv')


# In[23]:


df2.head()


# In[24]:


df2['DiagnosisOne'].isnull().sum()


# In[25]:


df2 = df2[pd.notnull(df2['DiagnosisOne'])]


# In[26]:


new_input = df2['DiagnosisOne']


# In[27]:


new_output = rnd.predict(count_vect.transform(new_input))


# In[28]:


df2['Condition'] = new_output


# In[29]:


df2


# In[30]:


df2['Condition'].nunique()


# In[31]:


fig = plt.figure(figsize=(10,6))
df2.groupby('Condition').DiagnosisOne.count().plot.bar(ylim=0)
plt.show()


# In[32]:


# Random manual check for "UTI" in both datasets discovered that a lot of simple descriptions in column "DiagnosisOne"
# didn't correspond to the "Urinary Tract Infection" in the original dataset. It is beyond the scope of this
# assignment, but as a first step before making predictive models I would make sure to ask questions and understand
# reason behind discrepancies in the original dataset.


# In[33]:


df2.to_csv('Holdout_Prediction.csv', index=None)


# In[ ]:




