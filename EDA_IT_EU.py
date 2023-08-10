#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from scipy import stats as sts
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


delete_office_days = df[df['home_office_days_monthly'] > 20].index


# In[18]:


df.drop(delete_office_days, inplace = True)


# In[19]:


duration_counts = df['contract_duration'].value_counts()
print(duration_counts)


# In[20]:


df['contract_duration'].fillna('unlimited', inplace = True) 

# There is a huge majority of unlimited contracts so I've decided to fill nulls with those type of contracts 
# (It won't disturb data distribution between those options)


# In[21]:


df['company_size'].replace('Oct-50', '10-50', inplace = True) 
# based on ranges in company sizes I've come to an conclusion that 'Oct - 50' means '10 - 50' cause of lack of this range


# In[22]:


size_counts = df['company_size'].value_counts()
size_counts


# In[23]:


df['company_size'].fillna('1000+', inplace = True) 

# Assusmed that there is a lot of respondents from companies with more than a 1000 employees


# In[24]:


# Assumption: Bonus and stocks were not filled cause people didn't have those
# Solution: Filled NaNs in bonus and stocks with zeros


# In[25]:


df['yearly_bonus'].fillna(0, inplace = True)
df['yearly_stocks'].fillna(0, inplace = True)
df['yearly_bonus_2018'].fillna(0, inplace = True)
df['yearly_stocks_2018'].fillna(0, inplace = True)


# In[26]:


# got indexes where fields are not filled to delete those rows 
# (these are the more specific features which fixing could be ineffective to fill with values):


# In[27]:


no_salary = df[df['yearly_brutto_salary_2018'].isna()].index


# In[28]:


df.drop(no_salary, axis = 0, inplace = True)


# In[29]:


no_seniority = df[df['seniority'].isna()].index
df.drop(no_seniority, axis = 0, inplace = True)


# In[30]:


no_technology = df[df['main_technology'].isna()].index
df.drop(no_technology, axis = 0, inplace = True)


# In[31]:


no_company_type = df[df['company_type'].isna()].index
df.drop(no_company_type, axis = 0, inplace = True)


# In[32]:


no_business_industry = df[df['business_industry'].isna()].index
df.drop(no_business_industry, axis = 0, inplace = True)


# In[33]:


df.reset_index(inplace = True)


# In[34]:


df.head()


# In[35]:


df.drop(['index'], axis = 1, inplace = True) # drop old index


# Numerical data - changing data types

# In[36]:


df.select_dtypes(include = ['int', 'float'])


# In[37]:


df['vacation_days'] = df['vacation_days'].astype(int)


# In[38]:


delete_days = df[df['vacation_days'] > 50].index


# In[39]:


df.drop(delete_days, inplace = True)


# In[40]:


df['age'].unique()


# In[41]:


df['age'] = df['age'].astype(int)


# In[42]:


df['yearly_brutto_salary'] = df['yearly_brutto_salary'].astype(int)
df['yearly_brutto_salary_2018'] = df['yearly_brutto_salary_2018'].astype(int)


# In[43]:


df['yearly_bonus'] = df['yearly_bonus'].astype(int)
df['yearly_bonus_2018'] = df['yearly_bonus'].astype(int)


# In[44]:


df.select_dtypes(include = ['int', 'float'])


# In[45]:


df.head()


# Categorical data - looking fo errors

# In[46]:


df['work_language'].unique()


# In[47]:


# Simplifying main languages put into form by respondents


# In[48]:


df['work_language'].replace('Deutsch', 'German', inplace = True)
df['work_language'].replace('English+Deutsch', 'English', inplace = True)
df['work_language'].replace('Polish+English', 'English', inplace = True)


# In[49]:


df['company_type'].unique()


# In[50]:


df['business_industry'].unique()


# In[51]:


df['seniority'].unique()


# In[52]:


df['position'].unique()


# In[53]:


city_list = df['city'].unique()
city_list


# In[54]:


df['city'].replace('Bayern', 'Munich', inplace = True) # replacing name of the city based on domain knowledge


# In[55]:


df['city'].replace('Würzburg ', 'Würzburg', inplace = True)
df['city'].replace('Kassel ', 'Kassel', inplace = True)


# In[56]:


df['city'].unique()


# In[57]:


df['gender'].unique()


# In[58]:


df['main_technology'].value_counts() # quick look at the technologies used (looking for duplicates)


# Columns standarization and final form

# In[59]:


df.rename(columns = {'yearly_brutto_salary': 'yearly_brutto_salary_eur_2019', 
                    'yearly_bonus': 'yearly_bonus_eur_2019', 
                    'yearly_brutto_salary_2018': 'yearly_brutto_salary_eur_2018', 
                     'yearly_bonus_2018': 'yearly_bonus_eur_2018'}, inplace = True)


# In[60]:


df.head()


# In[61]:


df['main_technology'] = df.main_technology.astype('category')


# In[62]:


type(df['main_technology'])


# In[63]:


df[df['contract_duration'] == '3 month']


# In[64]:


df[(df['city'] == 'Munich') | (df['city'] == 'Berlin')] 


# In[65]:


print(df.dtypes)


# In[66]:


df.info()


# In[67]:


df.to_csv(r'C:\Users\jsmvk\Desktop\projects\eda project\IT_Salary_Survey_EU_2019.csv', index = False)


# # Exploratory Data Analysis

# In[68]:


import matplotlib.pyplot as plt
import scipy.stats as scp


# In[69]:


df.describe()


# ## Estimates of location

# In[70]:


df['experience_years'].unique()


# In[71]:


np.median(df['age'])


# In[72]:


np.average(df['experience_years'], weights=df['yearly_brutto_salary_eur_2019'])


# In[73]:


plt.boxplot(df['yearly_brutto_salary_eur_2019'])
plt.ylabel('2019 salary')


# In[74]:


scp.trim_mean(df['yearly_brutto_salary_eur_2019'], proportiontocut=0.2)


# In[75]:


np.median(df['yearly_brutto_salary_eur_2019'])


# In[76]:


df['yearly_bonus_eur_2019'].unique()


# In[77]:


df['yearly_bonus_eur_2019'].value_counts()


# In[78]:


np.median(df['yearly_bonus_eur_2019'])


# In[79]:


plt.boxplot(df['yearly_bonus_eur_2019'])
plt.ylabel('2019 bonus')


# In[80]:


np.median(df['yearly_stocks'])


# In[81]:


np.median(df['yearly_brutto_salary_eur_2018'])


# In[82]:


np.median(df['yearly_bonus_eur_2018'])


# In[83]:


np.median(df['yearly_stocks_2018'])


# In[84]:


plt.boxplot(df['vacation_days'])
plt.ylabel('vacation days a year')


# In[85]:


np.median(df['vacation_days'])


# In[86]:


plt.boxplot(df['home_office_days_monthly'])
plt.ylabel('home office days monthly')


# In[87]:


np.median(df['home_office_days_monthly'])


# ## Estimates of variability

# In[88]:


df.head()


# In[89]:


max(df['yearly_stocks'])


# In[90]:


np.var(df['age'])


# In[91]:


np.var(df['experience_years'])


# In[92]:


np.var(df['yearly_brutto_salary_eur_2019'])


# In[93]:


df.mad() # mean absolute distribution


# In[94]:


np.var(df['yearly_brutto_salary_eur_2018'])


# In[95]:


np.var(df['vacation_days'])


# In[96]:


np.var(df['home_office_days_monthly'])


# ## Data distribution

# In[97]:


df.head()


# In[98]:


df['experience_years'].min()


# In[99]:


df['experience_years'].max()


# In[100]:


sns.histplot(df['experience_years'], bins = 6, kde = True)


# In[101]:


sns.histplot(df['yearly_brutto_salary_eur_2019'], kde = True)


# In[102]:


sns.histplot(df['yearly_brutto_salary_eur_2018'], kde = True)


# In[103]:


sns.countplot(y = df['main_technology'],
              order = df['main_technology'].value_counts().iloc[:10].index)


# In[104]:


sns.countplot(y = df['main_technology'],
              order = df['main_technology'].value_counts().iloc[-16:-1].index)


# In[105]:


sns.countplot(y = df['city'], 
             order = df['city'].value_counts().iloc[:10].index)


# In[166]:


df['city'].unique()


# In[169]:


len(df[df['city'] == ('Berlin' or 'Frankfurt' or 'Munich' or 'Hamburg' or 'Leipzig' or 'Nuremberg' or 'Cologne'
                 or 'Stuttgart' or 'Karlsruhe' or 
                'Bern' or 'Düsseldorf' or 'Pforzheim'
                  or 'Kassel' or 'Vienna' or'Hannover' or 'Heidelberg'
                 or 'Bielefeld' or 'Lingen' or 'Dresden' or 'Schleswig-Holstein'
                 or 'Kaiserslautern' or 'Würzburg' or 'Bremen')])


# In[106]:


sns.countplot(x = df['gender'])


# In[107]:


sns.countplot(x = df['seniority'], order = df['seniority'].value_counts().index)


# In[108]:


sns.histplot(df['age'], kde = True)


# In[109]:


sns.countplot(y = df['position'], order = df['position'].value_counts().iloc[:10].index)


# In[110]:


sns.histplot(df['vacation_days'], kde = True)


# In[111]:


sns.boxplot(df['home_office_days_monthly'])


# In[112]:


sns.countplot(df['work_language'])


# In[162]:


df[['city', 'work_language', 
    'yearly_brutto_salary_eur_2018', 
    'yearly_brutto_salary_eur_2019', 'yearly_salary_mean']][df['work_language'] == 'Italian']


# In[158]:


len(df[df['work_language'] == 'German'])


# In[159]:


len(df[df['work_language'] == 'English'])


# In[165]:


len(df[df['work_language'] == 'French'])


# In[113]:


sns.countplot(df['company_size'], order = df['company_size'].value_counts().index)


# In[114]:


sns.countplot(y = df['company_type'], order = df['company_type'].value_counts().index)


# In[115]:


sns.countplot(y = df['contract_duration'])


# In[116]:


sns.countplot(y = df['business_industry'], order = df['business_industry'].value_counts().iloc[:10].index)


# In[117]:


sns.histplot(df['yearly_stocks'], kde = True)


# In[118]:


sns.histplot(df['yearly_stocks_2018'], kde = True)


# In[119]:


sns.histplot(df['yearly_bonus_eur_2018'], kde = True)


# In[120]:


sns.histplot(df['yearly_bonus_eur_2019'], kde = True)


# ## Correlation

# In[121]:


df.corr()


# In[122]:


sns.pairplot(df, hue = 'seniority', 
             vars = ['experience_years', 'age', 'yearly_brutto_salary_eur_2018', 'yearly_brutto_salary_eur_2019'])


# In[123]:


sts.pearsonr(df['experience_years'], df['yearly_brutto_salary_eur_2018'])


# ## Business insight

# In[124]:


np.median(df['yearly_brutto_salary_eur_2018']) * 1.5


# In[125]:


(len(df[df['yearly_brutto_salary_eur_2018'] > np.median(df['yearly_brutto_salary_eur_2018']) * 1.5]) / 525) * 100
# percentage of people earning 1.5 * median


# In[126]:


df.info()


# In[127]:


df_mean = df[['yearly_brutto_salary_eur_2018', 'yearly_brutto_salary_eur_2019']]
df['yearly_salary_mean'] = np.mean(df_mean, axis = 1)


# In[128]:


df_salary = df[['yearly_salary_mean', 'company_size']]
df_salary = df_salary.groupby(['company_size']).mean().sort_values('yearly_salary_mean', ascending = False)
df_salary


# In[129]:


df_salary['company_size'] = df_salary.index


# In[130]:


plt.bar(df_salary['company_size'], df_salary['yearly_salary_mean'])
plt.xlabel('company size')
plt.ylabel('yearly salary mean')
plt.ylim(60000, 75000)


# In[231]:


len(df_technology)


# In[236]:


df_top_excluded = df[['main_technology', 'yearly_salary_mean']]
df_top_excluded = df_technology.groupby('main_technology').mean().nsmallest(26, 'yearly_salary_mean').sort_values(
    'yearly_salary_mean', ascending = False)


# In[237]:


df_top_excluded['main_technology'] = df_excluded.index 


# In[301]:


df_technology_top = df_technology.nlargest(5, 'yearly_salary_mean')


# In[302]:


median_top_excluded = np.median(df_excluded['yearly_salary_mean'])
median_top = np.median(df_technology_top['yearly_salary_mean']) 


# In[304]:


median_top


# In[305]:


median_top_excluded


# In[306]:


median_top / median_top_excluded # median of top 5 


# In[132]:


df_technology['main_technology'] = df_technology.index 


# In[133]:


plt.bar(df_technology['main_technology'], df_technology['yearly_salary_mean'])
plt.xlabel('technology')
plt.ylabel('yearly salary mean')
plt.ylim(80000, 130000)


# In[134]:


df_small_technology = df[['main_technology', 'yearly_salary_mean']]
df_small_technology = df_small_technology.groupby('main_technology').mean().nsmallest(5, 'yearly_salary_mean')
df_small_technology


# In[135]:


df_small_technology['main_technology'] = df_small_technology.index
df_small_technology['main_technology'] = df_small_technology['main_technology'].replace("Linux-Stack, Networking", "Linux-Stack")


# In[136]:


plt.bar(df_small_technology['main_technology'], df_small_technology['yearly_salary_mean'])
plt.xlabel('technology')
plt.ylabel('yearly salary mean')
plt.ylim(0, 65000)


# In[137]:


df_language = df[['work_language', 'yearly_salary_mean']]
df_language = df_language.groupby('work_language').mean().sort_values('yearly_salary_mean', ascending = False)
df_language


# In[138]:


df_language['work_language'] = df_language.index


# In[139]:


plt.bar(df_language['work_language'], df_language['yearly_salary_mean'])
plt.xlabel('work language')
plt.ylabel('yearly salary mean')
plt.ylim(40000, 98000)


# In[140]:


df_company_type = df[['company_type', 'yearly_salary_mean']]
df_company_type = df_company_type.groupby('company_type').mean().sort_values('yearly_salary_mean', ascending = False)
df_company_type


# In[141]:


df_company_type['company_type'] = df_company_type.index


# In[142]:


df_company_type['company_type'] = df_company_type['company_type'].replace('Consulting / Agency', 'Consulting')
df_company_type['company_type'] = df_company_type['company_type'].replace('Bodyshop / Outsource', 'Outsource')


# In[273]:


df_company_type['type'] = df_company_type.index


# In[274]:


df_company_type.nsmallest(5, 'yearly_salary_mean')


# In[277]:


np.mean(df_company_type['yearly_salary_mean'])


# In[282]:


70348 / np.mean(df_company_type['yearly_salary_mean'])


# In[292]:


outsource_university_excluded = df_company_type[df_company_type['company_type'] != ('Outsource' and 'University')]


# In[293]:


np.mean(outsource_excluded['yearly_salary_mean']) / 58270.833333	


# In[294]:


university_outsource = df_company_type[df_company_type['company_type'] == ('Outsource' and 'University')]


# In[295]:


np.mean(outsource_university_excluded['yearly_salary_mean']) / np.mean(university_outsource['yearly_salary_mean'])


# In[288]:


plt.bar(df_company_type['company_type'], df_company_type['yearly_salary_mean'])
plt.xlabel('company type')
plt.ylabel('yearly salary mean')
plt.ylim(40000, 75000)


# In[ ]:





# In[144]:


df_industry = df[['business_industry', 'yearly_salary_mean']]
df_industry = df_industry.groupby('business_industry').mean().sort_values('yearly_salary_mean', ascending = False).nlargest(5, 'yearly_salary_mean')
df_industry


# In[145]:


df_industry['business_industry'] = df_industry.index


# In[146]:


plt.bar(df_industry['business_industry'], df_industry['yearly_salary_mean'])
plt.xlabel('industry')
plt.ylabel('yearly salary mean')
plt.ylim(70000, 110000)


# In[147]:


df_income = df[['yearly_bonus_eur_2019', 'yearly_bonus_eur_2018', 'yearly_stocks', 'yearly_stocks_2018']]
df['bonus_stocks_mean'] = np.mean(df_income, axis = 1)
df_additionl_income = df[['company_type', 'bonus_stocks_mean']]
df_additional_income = df_additionl_income.groupby('company_type').mean().sort_values('bonus_stocks_mean', ascending = False)
df_additional_income


# In[148]:


df_additional_income['company_type'] = df_additional_income.index


# In[149]:


df_additional_income['company_type'] = df_additional_income['company_type'].replace('Consulting / Agency', 'Consulting')
df_additional_income['company_type'] = df_additional_income['company_type'].replace('Bodyshop / Outsource', 'Outsource')


# In[150]:


plt.bar(df_additional_income['company_type'], df_additional_income['bonus_stocks_mean'])
plt.xlabel('comany type')
plt.ylabel('bonus stocks mean')
plt.ylim(0, 4000)


# In[151]:


df_income = df[['yearly_bonus_eur_2019', 'yearly_bonus_eur_2018', 'yearly_stocks', 'yearly_stocks_2018']]
df['bonus_stocks_mean'] = np.mean(df_income, axis = 1)
df_additional_income_size = df[['company_size', 'bonus_stocks_mean']]
df_additional_income_size = df_additional_income_size.groupby('company_size').mean().sort_values('bonus_stocks_mean', ascending = False)
df_additional_income_size


# In[171]:


df_additional_income_size['company_size'] = df_additional_income_size.index


# In[172]:


plt.bar(df_additional_income_size['company_size'], df_additional_income_size['bonus_stocks_mean'])
plt.xlabel('comany size')
plt.ylabel('bonus stocks mean')
plt.ylim(0, 4500)


# In[184]:


df[['bonus_stocks_mean', 'company_type', 'position', 'city', 'experience_years']][df['company_type'] == 'Bank']


# In[180]:


df.info()


# In[ ]:




