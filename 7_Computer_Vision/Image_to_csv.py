#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
import pytesseract
import re
import sys


# In[2]:


#arg = sys.argv[1]

arg = 'Img1.PNG'


# In[3]:


img = cv2.imread(arg)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


# In[4]:


plt.figure(figsize=(16,16))
plt.imshow(gray, cmap="gray")


# In[5]:


img.shape


# In[6]:


y1 =0
x1=0

h = img.shape[0]
w =img.shape[1] 

img_croped = img[15:y1+h, x1:x1+w]

crop_img_gray = gray[15:y1+h, x1:x1+w]

plt.figure(figsize=(16,16))

plt.imshow(crop_img_gray, cmap="gray")


# In[7]:


edges2 = cv2.Sobel(crop_img_gray, dx = 0, dy = 1, ksize = 3, ddepth= int())


# In[8]:


plt.figure(figsize=(14,14))
plt.imshow(edges2, cmap="gray")


# In[9]:


lines = cv2.HoughLinesP(image=edges2,rho=10,theta=np.pi/4, threshold=5,lines=np.array([]), minLineLength=400)

a,b,c = lines.shape

for i in range(a):
         
    cv2.line(img_croped , (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), ( 255,0,0), 3, cv2.LINE_AA)

    cv2.imwrite('hough.jpg', img_croped)
    
print(a,b,c)


# In[10]:


print(lines)


# In[11]:


img2 = cv2.imread('hough.jpg')


plt.figure(figsize=(16,16))
plt.imshow(img2)


# In[12]:


lines2 =lines.reshape(lines.shape[0],lines.shape[2])


# In[13]:


lines2 =lines2[lines2[:, 1].argsort()]


# In[14]:


for i in range(len(lines2)):
    if i+1 == lines2.shape[0]:
        break
    else:
        if abs(lines2[i+1][1]-lines2[i][1])<20:
            lines2 =np.delete(lines2, i, axis=0)
            


# In[15]:


lines2


# In[16]:


height =lines2[1][3] -lines2[0][1] 
print(height)


# In[17]:


print(x1, w)


# In[18]:


x_crop = x1
y_crop= lines2[0][1]


# In[19]:


width = w

print(f"x: {x_crop}, y: {y_crop}, width: {width}, height: {height}")


# In[20]:


img_before = cv2.imread("hough.jpg")

cropped = img_before[y_crop:y_crop+height, x_crop:width]


# In[21]:


plt.imshow(cropped)


# In[22]:


cv2.imwrite('trans.jpg',cropped )


# In[23]:


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# In[24]:


img = cv2.imread('trans.jpg')
plt.imshow(img)


# In[25]:


im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# In[26]:


plt.figure(figsize=(20,int(im.shape[1]/im.shape[0])))
plt.imshow(im)
plt.show()


# In[27]:


custom_config = r'-l eng --psm 6'
pytesseract.image_to_string(im, config=custom_config)


# In[28]:


text =pytesseract.image_to_string(im, config=custom_config)


# In[29]:


print(text)


# In[30]:


pattern_date =re.compile(r"\d+[/-]\d+[/-]\d+")

matches_date = pattern_date.findall(text)


# In[31]:


matches_date


# In[32]:


pattern_name = re.compile(r"(?<=\d )[A-Za-z]*(?= \d+)")

matches_name = pattern_name.findall(text)

matches_name


# In[33]:


type(matches_name)


# In[34]:


for i in matches_name:
    if i in text:
        text =text.replace(i,"")


# In[35]:


text


# In[36]:


for i in matches_date:
    text =text.replace(i,"")


# In[37]:


text


# In[38]:


pattern_desc =re.compile(r" \D.+? (?=\d+\.\d\d)")

matches_desc =pattern_desc.findall(text)


# In[39]:


matches_desc


# In[40]:


pattern_net =re.compile(r" -?\d+\.\d\d(?= \*\*|\n)")

matches_net =pattern_net.findall(text)


# In[41]:


matches_net


# In[55]:


InvoicePetName= matches_name*len(matches_net)

InvoicePetName


# In[48]:


matches_date = [i.replace("-","/") for i in matches_date]

print(matches_date)


# In[49]:


FileName =[arg]
print(FileName)
FileName = FileName*len(matches_date)
print(FileName)


# In[50]:


columns = {"InvoicePetName": InvoicePetName, "TransactionDate": matches_date, "ItemDescription":matches_desc,"NetPrice":matches_net, "FileName":FileName}  


# In[51]:


headers =[]
for key, value in columns.items() :
    headers.append(key)
print(headers)


# In[52]:


df = pd.DataFrame(columns)


# In[53]:


df


# In[54]:


df.to_csv("output.csv")

