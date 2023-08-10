import numpy as np
import pandas as pd
from scipy import stats as sts
import seaborn as sns

df = pd.read_csv('Desktop\projects\eda project\IT Salary Survey EU 2019.csv', sep = ",")

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

df.drop(['survey_time'], axis = 1, inplace = True) # dropping unnecessary column

len(df.index) # check number of rows

# Process of nulls elimination

print(df.isnull().sum()) # check number of nulls

df.drop('0', axis = 1, inplace = True) # dropping unnecessary column

df.drop('company_name', axis = 1, inplace = True) # dropping unnecessary column

#Columns: 
#work_language -> fill with "English" cause everyone speaks it
#Age -> fill with median of age
#vacation days -> fill nan with "0" (assumption that those who didn't fill that didn't use vacation days)
#office days monthly -> fill nan with median

df['age'].fillna(df['age'].median(), inplace = True)

df['work_language'].fillna("English", inplace = True)

df = df[df['position'].notna()]

df = df[df['yearly_brutto_salary'].notna()]

df['vacation_days'].fillna(0, inplace = True)

df['home_office_days_monthly'].fillna(32, inplace = True) #32 > days a month

df['home_office_days_monthly'] = df['home_office_days_monthly'].astype(int)

df['home_office_days_monthly'].replace(32, 0, inplace = True)

df['home_office_days_monthly'].replace(0, df['home_office_days_monthly'].median(), inplace = True)

df['home_office_days_monthly']

delete_office_days = df[df['home_office_days_monthly'] > 20].index

df.drop(delete_office_days, inplace = True)

duration_counts = df['contract_duration'].value_counts()
print(duration_counts)

df['contract_duration'].fillna('unlimited', inplace = True) 

# There is a majority of unlimited contracts so I've decided to fill nulls with those type of contracts 
# (It won't disturb data distribution between those options)

df['company_size'].replace('Oct-50', '10-50', inplace = True) 

# based on ranges in company sizes I've come to conclusion that 'Oct - 50' means '10 - 50' cause of lack of this range

size_counts = df['company_size'].value_counts()

df['company_size'].fillna('1000+', inplace = True) 

# Assusmed that there is a lot of respondents from companies with more than a 1000 employees

# Assumption: Bonus and stocks were not filled cause people didn't have those
# Solution: Filled NaNs in bonus and stocks with zeros

df['yearly_bonus'].fillna(0, inplace = True)

df['yearly_stocks'].fillna(0, inplace = True)

df['yearly_bonus_2018'].fillna(0, inplace = True)

df['yearly_stocks_2018'].fillna(0, inplace = True)

# got indexes where fields are not filled to delete those rows 
# (these are the more specific features which fixing could be ineffective to fill with values):

no_salary = df[df['yearly_brutto_salary_2018'].isna()].index

df.drop(no_salary, axis = 0, inplace = True)

no_seniority = df[df['seniority'].isna()].index

df.drop(no_seniority, axis = 0, inplace = True)

no_technology = df[df['main_technology'].isna()].index

df.drop(no_technology, axis = 0, inplace = True)

no_company_type = df[df['company_type'].isna()].index

df.drop(no_company_type, axis = 0, inplace = True)

no_business_industry = df[df['business_industry'].isna()].index

df.drop(no_business_industry, axis = 0, inplace = True)

df.reset_index(inplace = True)

df.drop(['index'], axis = 1, inplace = True) # drop old index

# Numerical data - changing data types

df.select_dtypes(include = ['int', 'float'])

df['vacation_days'] = df['vacation_days'].astype(int)

delete_days = df[df['vacation_days'] > 50].index

df.drop(delete_days, inplace = True)

df['age'].unique()

df['age'] = df['age'].astype(int)

df['yearly_brutto_salary'] = df['yearly_brutto_salary'].astype(int)

df['yearly_brutto_salary_2018'] = df['yearly_brutto_salary_2018'].astype(int)

df['yearly_bonus'] = df['yearly_bonus'].astype(int)

df['yearly_bonus_2018'] = df['yearly_bonus'].astype(int)

df.select_dtypes(include = ['int', 'float'])

# Categorical data - looking fo errors

df['work_language'].unique() # Simplifying main languages put into form by respondents

df['work_language'].replace('Deutsch', 'German', inplace = True)

df['work_language'].replace('English+Deutsch', 'English', inplace = True)

df['work_language'].replace('Polish+English', 'English', inplace = True)

df['company_type'].unique()

df['business_industry'].unique()

df['seniority'].unique()

df['position'].unique()

city_list = df['city'].unique()

df['city'].replace('Bayern', 'Munich', inplace = True) # replacing name of the city based on domain knowledge

df['city'].replace('Würzburg ', 'Würzburg', inplace = True)

df['city'].replace('Kassel ', 'Kassel', inplace = True)

df['city'].unique()

df['gender'].unique()

df['main_technology'].value_counts() # quick look at the technologies used (looking for duplicates)

# Columns standarization and final form

df.rename(columns = {'yearly_brutto_salary': 'yearly_brutto_salary_eur_2019', 
                    'yearly_bonus': 'yearly_bonus_eur_2019', 
                    'yearly_brutto_salary_2018': 'yearly_brutto_salary_eur_2018', 
                     'yearly_bonus_2018': 'yearly_bonus_eur_2018'}, inplace = True)

df['main_technology'] = df.main_technology.astype('category')

type(df['main_technology'])

df[df['contract_duration'] == '3 month']

df[(df['city'] == 'Munich') | (df['city'] == 'Berlin')] 

print(df.dtypes)

df.to_csv(r'C:\Users\jsmvk\Desktop\projects\eda project\IT_Salary_Survey_EU_2019.csv', index = False)

# Exploratory Data Analysis

import matplotlib.pyplot as plt
import scipy.stats as scp

df.describe()

# Estimates of location

df['experience_years'].unique()

np.median(df['age'])

np.average(df['experience_years'], weights=df['yearly_brutto_salary_eur_2019'])

plt.boxplot(df['yearly_brutto_salary_eur_2019'])
plt.ylabel('2019 salary')

scp.trim_mean(df['yearly_brutto_salary_eur_2019'], proportiontocut=0.2)

np.median(df['yearly_brutto_salary_eur_2019'])

df['yearly_bonus_eur_2019'].unique()

df['yearly_bonus_eur_2019'].value_counts()

np.median(df['yearly_bonus_eur_2019'])

plt.boxplot(df['yearly_bonus_eur_2019'])

plt.ylabel('2019 bonus')

np.median(df['yearly_stocks'])

np.median(df['yearly_brutto_salary_eur_2018'])

np.median(df['yearly_bonus_eur_2018'])

np.median(df['yearly_stocks_2018'])

plt.boxplot(df['vacation_days'])

plt.ylabel('vacation days a year')

np.median(df['vacation_days'])

plt.boxplot(df['home_office_days_monthly'])

plt.ylabel('home office days monthly')

np.median(df['home_office_days_monthly'])

# Estimates of variability

max(df['yearly_stocks'])

np.var(df['age'])

np.var(df['experience_years'])

np.var(df['yearly_brutto_salary_eur_2019'])

df.mad() # mean absolute distribution

np.var(df['yearly_brutto_salary_eur_2018'])

np.var(df['vacation_days'])

np.var(df['home_office_days_monthly'])

# Data distribution

df['experience_years'].min()
df['experience_years'].max()

sns.histplot(df['experience_years'], bins = 6, kde = True)

sns.histplot(df['yearly_brutto_salary_eur_2019'], kde = True)

sns.histplot(df['yearly_brutto_salary_eur_2018'], kde = True)

sns.countplot(y = df['main_technology'],
              order = df['main_technology'].value_counts().iloc[:10].index)

sns.countplot(y = df['main_technology'],
              order = df['main_technology'].value_counts().iloc[-16:-1].index)

sns.countplot(y = df['city'], 
             order = df['city'].value_counts().iloc[:10].index)

df['city'].unique()

len(df[df['city'] == ('Berlin' or 'Frankfurt' or 'Munich' or 'Hamburg' or 'Leipzig' or 'Nuremberg' or 'Cologne'
                 or 'Stuttgart' or 'Karlsruhe' or 
                'Bern' or 'Düsseldorf' or 'Pforzheim'
                  or 'Kassel' or 'Vienna' or'Hannover' or 'Heidelberg'
                 or 'Bielefeld' or 'Lingen' or 'Dresden' or 'Schleswig-Holstein'
                 or 'Kaiserslautern' or 'Würzburg' or 'Bremen')])

sns.countplot(x = df['gender'])

sns.countplot(x = df['seniority'], order = df['seniority'].value_counts().index)

sns.histplot(df['age'], kde = True)

sns.countplot(y = df['position'], order = df['position'].value_counts().iloc[:10].index)

sns.histplot(df['vacation_days'], kde = True)

sns.boxplot(df['home_office_days_monthly'])

sns.countplot(df['work_language'])

df[['city', 'work_language', 
    'yearly_brutto_salary_eur_2018', 
    'yearly_brutto_salary_eur_2019', 'yearly_salary_mean']][df['work_language'] == 'Italian']

len(df[df['work_language'] == 'German'])

len(df[df['work_language'] == 'English'])

len(df[df['work_language'] == 'French'])

sns.countplot(df['company_size'], order = df['company_size'].value_counts().index)

sns.countplot(y = df['company_type'], order = df['company_type'].value_counts().index)

sns.countplot(y = df['contract_duration'])

sns.countplot(y = df['business_industry'], order = df['business_industry'].value_counts().iloc[:10].index)

sns.histplot(df['yearly_stocks'], kde = True)

sns.histplot(df['yearly_stocks_2018'], kde = True)

sns.histplot(df['yearly_bonus_eur_2018'], kde = True)

sns.histplot(df['yearly_bonus_eur_2019'], kde = True)

# Correlation

df.corr()

sns.pairplot(df, hue = 'seniority', 
             vars = ['experience_years', 'age', 'yearly_brutto_salary_eur_2018', 'yearly_brutto_salary_eur_2019'])

sts.pearsonr(df['experience_years'], df['yearly_brutto_salary_eur_2018'])

# Business insight

np.median(df['yearly_brutto_salary_eur_2018']) * 1.5

(len(df[df['yearly_brutto_salary_eur_2018'] > np.median(df['yearly_brutto_salary_eur_2018']) * 1.5]) / 525) * 100
# percentage of people earning 1.5 * median

df_mean = df[['yearly_brutto_salary_eur_2018', 'yearly_brutto_salary_eur_2019']]
df['yearly_salary_mean'] = np.mean(df_mean, axis = 1)
df_salary = df[['yearly_salary_mean', 'company_size']]
df_salary = df_salary.groupby(['company_size']).mean().sort_values('yearly_salary_mean', ascending = False)
df_salary['company_size'] = df_salary.index

plt.bar(df_salary['company_size'], df_salary['yearly_salary_mean'])
plt.xlabel('company size')
plt.ylabel('yearly salary mean')
plt.ylim(60000, 75000)

len(df_technology)

df_top_excluded = df[['main_technology', 'yearly_salary_mean']]

df_top_excluded = df_technology.groupby('main_technology').mean().nsmallest(26, 'yearly_salary_mean').sort_values(
    'yearly_salary_mean', ascending = False)
df_top_excluded['main_technology'] = df_excluded.index 

df_technology_top = df_technology.nlargest(5, 'yearly_salary_mean')

median_top_excluded = np.median(df_excluded['yearly_salary_mean'])
median_top = np.median(df_technology_top['yearly_salary_mean']) 

median_top / median_top_excluded # median of top 5 

df_technology['main_technology'] = df_technology.index 

plt.bar(df_technology['main_technology'], df_technology['yearly_salary_mean'])
plt.xlabel('technology')
plt.ylabel('yearly salary mean')
plt.ylim(80000, 130000)

df_small_technology = df[['main_technology', 'yearly_salary_mean']]
df_small_technology = df_small_technology.groupby('main_technology').mean().nsmallest(5, 'yearly_salary_mean')
df_small_technology

df_small_technology['main_technology'] = df_small_technology.index

df_small_technology['main_technology'] = df_small_technology['main_technology'].replace("Linux-Stack, Networking", "Linux-Stack")

plt.bar(df_small_technology['main_technology'], df_small_technology['yearly_salary_mean'])
plt.xlabel('technology')
plt.ylabel('yearly salary mean')
plt.ylim(0, 65000)

df_language = df[['work_language', 'yearly_salary_mean']]

df_language = df_language.groupby('work_language').mean().sort_values('yearly_salary_mean', ascending = False)

df_language['work_language'] = df_language.index

plt.bar(df_language['work_language'], df_language['yearly_salary_mean'])
plt.xlabel('work language')
plt.ylabel('yearly salary mean')
plt.ylim(40000, 98000)

df_company_type = df[['company_type', 'yearly_salary_mean']]
df_company_type = df_company_type.groupby('company_type').mean().sort_values('yearly_salary_mean', ascending = False)
df_company_type['company_type'] = df_company_type.index
df_company_type['company_type'] = df_company_type['company_type'].replace('Consulting / Agency', 'Consulting')
df_company_type['company_type'] = df_company_type['company_type'].replace('Bodyshop / Outsource', 'Outsource')
df_company_type['type'] = df_company_type.index
df_company_type.nsmallest(5, 'yearly_salary_mean')

np.mean(df_company_type['yearly_salary_mean'])

70348 / np.mean(df_company_type['yearly_salary_mean'])

outsource_university_excluded = df_company_type[df_company_type['company_type'] != ('Outsource' and 'University')]
np.mean(outsource_excluded['yearly_salary_mean']) / 58270.833333	
university_outsource = df_company_type[df_company_type['company_type'] == ('Outsource' and 'University')]
np.mean(outsource_university_excluded['yearly_salary_mean']) / np.mean(university_outsource['yearly_salary_mean'])

plt.bar(df_company_type['company_type'], df_company_type['yearly_salary_mean'])
plt.xlabel('company type')
plt.ylabel('yearly salary mean')
plt.ylim(40000, 75000)

df_industry = df[['business_industry', 'yearly_salary_mean']]
df_industry = df_industry.groupby('business_industry').mean().sort_values('yearly_salary_mean', ascending = False).nlargest(5, 'yearly_salary_mean')
df_industry['business_industry'] = df_industry.index

plt.bar(df_industry['business_industry'], df_industry['yearly_salary_mean'])
plt.xlabel('industry')
plt.ylabel('yearly salary mean')
plt.ylim(70000, 110000)

df_income = df[['yearly_bonus_eur_2019', 'yearly_bonus_eur_2018', 'yearly_stocks', 'yearly_stocks_2018']]

df['bonus_stocks_mean'] = np.mean(df_income, axis = 1)

df_additionl_income = df[['company_type', 'bonus_stocks_mean']]
df_additional_income = df_additionl_income.groupby('company_type').mean().sort_values('bonus_stocks_mean', ascending = False)
df_additional_income['company_type'] = df_additional_income.index
df_additional_income['company_type'] = df_additional_income['company_type'].replace('Consulting / Agency', 'Consulting')
df_additional_income['company_type'] = df_additional_income['company_type'].replace('Bodyshop / Outsource', 'Outsource')

plt.bar(df_additional_income['company_type'], df_additional_income['bonus_stocks_mean'])
plt.xlabel('comany type')
plt.ylabel('bonus stocks mean')
plt.ylim(0, 4000)


df_income = df[['yearly_bonus_eur_2019', 'yearly_bonus_eur_2018', 'yearly_stocks', 'yearly_stocks_2018']]
df['bonus_stocks_mean'] = np.mean(df_income, axis = 1)

df_additional_income_size = df[['company_size', 'bonus_stocks_mean']]
df_additional_income_size = df_additional_income_size.groupby('company_size').mean().sort_values('bonus_stocks_mean', ascending = False)
df_additional_income_size['company_size'] = df_additional_income_size.index

plt.bar(df_additional_income_size['company_size'], df_additional_income_size['bonus_stocks_mean'])
plt.xlabel('comany size')
plt.ylabel('bonus stocks mean')
plt.ylim(0, 4500)

df[['bonus_stocks_mean', 'company_type', 'position', 'city', 'experience_years']][df['company_type'] == 'Bank']
