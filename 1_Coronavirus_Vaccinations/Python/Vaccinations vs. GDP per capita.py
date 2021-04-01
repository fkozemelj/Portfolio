# Import necessary libraries
import numpy as np
import pandas as pd
import datetime as dt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# ## Importing and cleaning vaccination data


#Read the vaccinations data
country_vaccinations = pd.read_csv('C:/Users/fkoze/Desktop/Data_Science/Projects/Covid/country_vaccinations.csv')
country_vaccinations.head()

#Examine column attributes of the data set
print(country_vaccinations.columns)

#Check the number of rows and columns
country_vaccinations.shape

#Check for missing data 
country_vaccinations.isna().sum()

#Dropping columns that are not required for any analysis, here source_name and source_website
country_vaccinations.drop(['source_name', 'source_website'], axis = 1, inplace = True)
country_vaccinations.head()

#Check the value counts in country column
country_vaccinations.value_counts('country')

#In country column, England,Scotland,Northern Ireland and Wales are part of UK, let us drop rows except UK
index_names = country_vaccinations[country_vaccinations.country.isin(['England', 'Scotland', 'Wales', 'Northern Ireland'])].index
country_vaccinations.drop(index_names, inplace = True)

#Extract number of vaccinations per capita for each country
country_vaccinations_grouped = country_vaccinations.groupby('country', as_index = False).total_vaccinations_per_hundred.max()
country_vaccinations_grouped.head()



# ## Importing and cleaning GDP data


#Read the GDP data
country_gdp = pd.read_csv('C:/Users/fkoze/Desktop/Data_Science/Projects/Covid/GDP_per_capita.csv')
country_gdp.head()

#Using describe to get the basic parameters of the data set
country_gdp.describe(include='all')

#Dropping rows with some data missing
country_gdp = country_gdp.dropna()
country_gdp.shape


# ## Linear Regression


#Merging two different data sets
country_merged = pd.merge(country_gdp, country_vaccinations_grouped, on='country') 
country_merged

#Declaring dependent variable
targets = country_merged['total_vaccinations_per_hundred']
#Declaring independent variable
inputs = country_merged['2019']

#Transforming array from 1D to 2D
inputs = inputs.values.reshape(-1,1)
inputs.shape

#Fitting the model
reg = LinearRegression()
reg.fit(inputs,targets)

#Point where estimated regression line crosses the y-axix
reg.intercept_

#Finding the regression coefficient
reg.coef_

#Checks the R-squared value of the regression
reg.score(inputs,targets)


# ## Scatter Plot


#Showing the scatter plot with a estimated regression line
plt.scatter(inputs, targets, color = "red")
plt.plot(inputs, reg.predict(inputs), color = "green")
plt.title("GDP Vaccinations vs. GDP per capita")
plt.xlabel("GDP")
plt.ylabel("Rate of vaccinations")
plt.show()

