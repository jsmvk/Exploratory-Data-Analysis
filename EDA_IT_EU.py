#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv('Desktop\projects\eda project\IT Salary Survey EU 2019.csv', sep = ",")


# In[2]:


df.head()


# In[3]:


df.columns


# # Data cleaning

# Standarization of column names

# In[4]:


df = df.rename(columns = {"Age": "age", "Gender": "gender", "City":"city", "Zeitstempel": "survey_time", 
          "Position (without seniority)": "position", 
          "Your main technology / programming language": "main_technology",
        "Years of experience":"experience_years",
        "Seniority level":"seniority",
         "Yearly brutto salary (without bonus and stocks)": "yearly_brutto_salary",
         "Yearly brutto salary (without bonus and stocks) one year ago. Only answer if staying in same country": "yearly_brutto_salary_2018",
         "Yearly bonus one year ago. Only answer if staying in same country": "yearly_bonus_2018",
       "Yearly stocks one year ago. Only answer if staying in same country": "yearly_stocks_2018",
         "Yearly stocks": "yearly_stocks",
         "Yearly bonus": "yearly_bonus",
         "Number of vacation days": "vacation_days",
         "Number of home office days per month": "home_office_days_monthly",
         "Main language at work": "work_language",
         "Company name ": "company_name", 
         "Company size": "company_size",
         "Company type": "company_type",
         "Сontract duration": "contract_duration",
         "Company business sector": "business_industry"})


# In[5]:


df.info()


# In[6]:


df.drop(['survey_time'], axis = 1, inplace = True) # dropping unnecessary column


# In[7]:


len(df.index) # check number of rows


# Process of nulls elimination

# In[8]:


print(df.isnull().sum()) # check number of nulls


# In[9]:


df.drop('0', axis = 1, inplace = True) # dropping unnecessary column


# In[10]:


df.drop('company_name', axis = 1, inplace = True) # dropping unnecessary column


# In[11]:


#Columns: 
#work_language -> fill with "English" cause everyone speaks it
#Age -> fill with median of age
#vacation days -> fill nan with "0" (assumption that those who didn't fill that didn't use vacation days)
#office days monthly -> fill nan with median


# In[12]:


df['age'].fillna(df['age'].median(), inplace = True)


# In[13]:


df['work_language'].fillna("English", inplace = True)


# In[14]:


df = df[df['position'].notna()]
df = df[df['yearly_brutto_salary'].notna()]


# In[15]:


df['vacation_days'].fillna(0, inplace = True)


# In[16]:


df['home_office_days_monthly'].fillna(32, inplace = True) #32 > days a month
df['home_office_days_monthly'] = df['home_office_days_monthly'].astype(int)
df['home_office_days_monthly'].replace(32, 0, inplace = True)
df['home_office_days_monthly'].replace(0, df['home_office_days_monthly'].median(), inplace = True)

df['home_office_days_monthly']


# In[17]:


duration_counts = df['contract_duration'].value_counts()
print(duration_counts)


# In[18]:


df['contract_duration'].fillna('unlimited', inplace = True) 

# There is a huge majority of unlimited contracts so I've decided to fill nulls with those type of contracts 
# (It won't disturb data distribution between those options)


# In[19]:


df['company_size'].replace('Oct-50', '10-50', inplace = True) 
# based on ranges in company sizes I've come to an conclusion that 'Oct - 50' means '10 - 50' cause of lack of this range


# In[20]:


size_counts = df['company_size'].value_counts()
size_counts


# In[21]:


df['company_size'].fillna('1000+', inplace = True) 

# Assusmed that there is a lot of respondents from companies with more than a 1000 employees


# In[22]:


# Assumption: Bonus and stocks were not filled cause people didn't have those
# Solution: Filled NaNs in bonus and stocks with zeros


# In[23]:


df['yearly_bonus'].fillna(0, inplace = True)
df['yearly_stocks'].fillna(0, inplace = True)
df['yearly_bonus_2018'].fillna(0, inplace = True)
df['yearly_stocks_2018'].fillna(0, inplace = True)


# In[24]:


# got indexes where fields are not filled to delete those rows 
# (these are the more specific features which fixing could be ineffective to fill with values):


# In[25]:


no_salary = df[df['yearly_brutto_salary_2018'].isna()].index


# In[26]:


df.drop(no_salary, axis = 0, inplace = True)


# In[27]:


no_seniority = df[df['seniority'].isna()].index
df.drop(no_seniority, axis = 0, inplace = True)


# In[28]:


no_technology = df[df['main_technology'].isna()].index
df.drop(no_technology, axis = 0, inplace = True)


# In[29]:


no_company_type = df[df['company_type'].isna()].index
df.drop(no_company_type, axis = 0, inplace = True)


# In[30]:


no_business_industry = df[df['business_industry'].isna()].index
df.drop(no_business_industry, axis = 0, inplace = True)


# In[31]:


df.reset_index(inplace = True)


# In[32]:


df.head()


# In[33]:


df.drop(['index'], axis = 1, inplace = True) # drop old index


# Numerical data - changing data types

# In[34]:


df.select_dtypes(include = ['int', 'float'])


# In[35]:


df['vacation_days'] = df['vacation_days'].astype(int)


# In[36]:


df['age'].unique()


# In[37]:


df['age'] = df['age'].astype(int)


# In[38]:


df['yearly_brutto_salary'] = df['yearly_brutto_salary'].astype(int)
df['yearly_brutto_salary_2018'] = df['yearly_brutto_salary_2018'].astype(int)


# In[39]:


df['yearly_bonus'] = df['yearly_bonus'].astype(int)
df['yearly_bonus_2018'] = df['yearly_bonus'].astype(int)


# In[40]:


df.select_dtypes(include = ['int', 'float'])


# In[41]:


df.head()


# Categorical data - looking fo errors

# In[42]:


df['work_language'].unique()


# In[43]:


# Simplifying main languages put into form by respondents


# In[44]:


df['work_language'].replace('Deutsch', 'German', inplace = True)
df['work_language'].replace('English+Deutsch', 'English', inplace = True)
df['work_language'].replace('Polish+English', 'English', inplace = True)


# In[45]:


df['company_type'].unique()


# In[46]:


df['business_industry'].unique()


# In[47]:


df['seniority'].unique()


# In[48]:


df['position'].unique()


# In[49]:


city_list = df['city'].unique()
city_list


# In[50]:


df['city'].replace('Bayern', 'Munich', inplace = True) # replacing name of the city based on domain knowledge


# In[51]:


df['city'].replace('Würzburg ', 'Würzburg', inplace = True)
df['city'].replace('Kassel ', 'Kassel', inplace = True)


# In[52]:


df['city'].unique()


# In[53]:


df['gender'].unique()


# In[54]:


df['main_technology'].value_counts() # quick look at the technologies used (looking for duplicates)


# Columns standarization and final form

# In[55]:


df.rename(columns = {'yearly_brutto_salary': 'yearly_brutto_salary_eur_2019', 
                    'yearly_bonus': 'yearly_bonus_eur_2019', 
                    'yearly_brutto_salary_2018': 'yearly_brutto_salary_eur_2018', 
                     'yearly_bonus_2018': 'yearly_bonus_eur_2018'}, inplace = True)


# In[56]:


df.head()


# In[57]:


df['main_technology'] = df.main_technology.astype('category')


# In[58]:


type(df['main_technology'])


# In[59]:


print(df.dtypes)


# In[144]:


df.info()


# In[60]:


df.to_csv(r'C:\Users\jsmvk\Desktop\projects\eda project\IT_Salary_Survey_EU_2019.csv', index = False)


# # Exploratory Data Analysis

# In[61]:


# For every variable if apply:
# 1.Estimates of location
# 2.Estimates of variability
# 3.Data distribution
# 4.Categorical data
# 5.Correlation
# 6.Multivariete analysis

# target variable (y) to the rest (x)
# visualisation of salary through map
# pca
# + machine learning model
# others predictions google


# In[62]:


import matplotlib.pyplot as plt
import scipy.stats as scp


# ## Estimates of location

# In[63]:


np.mean(df['age'])


# In[64]:


df['experience_years'].unique()


# In[65]:


np.average(df['experience_years'], weights=df['yearly_brutto_salary_eur_2019'])


# In[66]:


np.mean(df['experience_years'])


# In[67]:


plt.boxplot(df['yearly_brutto_salary_eur_2019'])


# In[68]:


scp.trim_mean(df['yearly_brutto_salary_eur_2019'], proportiontocut=0.2)


# In[69]:


np.mean(df['yearly_brutto_salary_eur_2019'])


# In[70]:


np.median(df['yearly_brutto_salary_eur_2019'])


# In[71]:


df['yearly_bonus_eur_2019'].unique()


# In[72]:


df['yearly_bonus_eur_2019'].value_counts()


# In[73]:


np.median(df['yearly_bonus_eur_2019'])


# In[74]:


plt.boxplot(df['yearly_bonus_eur_2019'])


# In[75]:


np.median(df['yearly_stocks'])


# In[76]:


np.mean(df['yearly_brutto_salary_eur_2018'])


# In[77]:


np.median(df['yearly_brutto_salary_eur_2018'])


# In[78]:


np.median(df['yearly_bonus_eur_2018'])


# In[79]:


np.median(df['yearly_stocks_2018'])


# In[80]:


plt.boxplot(df['vacation_days'])


# In[81]:


np.median(df['vacation_days'])


# In[82]:


np.mean(df['vacation_days'])


# In[83]:


plt.boxplot(df['home_office_days_monthly'])


# In[84]:


np.median(df['home_office_days_monthly'])


# ## Estimates of variability

# In[85]:


df.head()


# In[86]:


np.std(df['age'])


# In[87]:


np.var(df['age'])


# In[88]:


np.std(df['experience_years'])


# In[89]:


np.var(df['experience_years'])


# In[90]:


np.std(df['yearly_brutto_salary_eur_2019'])


# In[91]:


np.var(df['yearly_brutto_salary_eur_2019'])


# In[92]:


df.mad() # mean absolute distribution


# In[93]:


np.var(df['yearly_brutto_salary_eur_2018'])


# In[94]:


np.var(df['vacation_days'])


# In[95]:


np.var(df['home_office_days_monthly'])


# ## Data distribution

# In[96]:


df.head()


# In[97]:


df['experience_years'].min()


# In[98]:


df['experience_years'].max()


# In[99]:


sns.histplot(df['experience_years'], bins = 6, kde = True)


# In[100]:


sns.histplot(df['yearly_brutto_salary_eur_2019'], kde = True)


# In[101]:


sns.histplot(df['yearly_brutto_salary_eur_2018'], kde = True)


# In[102]:


sns.countplot(y = df['main_technology'],
              order = df['main_technology'].value_counts().iloc[:10].index)


# In[103]:


sns.countplot(y = df['city'], 
             order = df['city'].value_counts().iloc[:10].index)


# In[104]:


sns.countplot(x = df['gender'])


# In[105]:


sns.countplot(x = df['seniority'])


# In[106]:


sns.histplot(df['age'], kde = True)


# In[111]:


sns.countplot(y = df['position'], order = df['position'].value_counts().iloc[:10].index)


# In[112]:


sns.histplot(df['vacation_days'], kde = True)


# In[117]:


sns.boxplot(df['home_office_days_monthly'])


# In[118]:


sns.countplot(df['work_language'])


# In[124]:


sns.countplot(df['company_size'])


# In[126]:


sns.countplot(y = df['company_type'])


# In[128]:


sns.countplot(y = df['contract_duration'])


# In[137]:


sns.countplot(y = df['business_industry'], order = df['business_industry'].value_counts().iloc[:10].index)


# In[138]:


sns.histplot(df['yearly_stocks'], kde = True)


# In[140]:


sns.histplot(df['yearly_stocks_2018'], kde = True)


# In[142]:


sns.histplot(df['yearly_bonus_eur_2018'], kde = True)


# In[143]:


sns.histplot(df['yearly_bonus_eur_2019'], kde = True)


# In[ ]:




