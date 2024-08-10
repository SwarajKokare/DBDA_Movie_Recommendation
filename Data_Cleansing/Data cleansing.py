#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import glob


# ### Combining csv files to get one csv

# In[2]:


csv_files_path = 'Movie_data_*.csv'
csv_files = glob.glob(csv_files_path)
csv_files


# In[3]:


dataframes = []
for file in csv_files:
    df = pd.read_csv(file,encoding='UTF8')
    dataframes.append(df)


# In[4]:


combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined dataframe to a new CSV file if desired
combined_df.to_csv('Movie_data.csv', index=False)
combined_df.head()


# ## Loading the new combined csv into a dataframe

# In[5]:


df1 = pd.read_csv("./Movie_data.csv")
df1.head()


# In[6]:


df1.info()


# ## Data Cleansing

# ### Removing null values:

# In[7]:


df1.isna().sum()


# In[8]:


df1.dropna(inplace=True,ignore_index=True)


# In[9]:


df1.info()


# In[10]:


df1['Plot synopsis'].isna().sum()


# ### Removing duplicate values:

# In[11]:


## Considering plot synopsis as it is unique for every movie while movie titles might be same for some movies.
df1['Plot synopsis'].is_unique


# In[12]:


## Checking duplicates
duplicates = df1[df1.duplicated(subset=['Plot synopsis'], keep=False)]
print(duplicates)


# In[13]:


# Removing duplicate:
df1['Plot synopsis'] = df1['Plot synopsis'].str.strip()
df_new = df1.drop_duplicates(subset=['Plot synopsis'],ignore_index=True)
print(df_new['Plot synopsis'].is_unique)


# In[14]:


df_new.info()


# ### Modifying the user votes as it is in object format:

# In[15]:


def modify_user_votes(x):
    if x[-1] == 'K':
        return float(x[:-1]) * 1000
    elif x[-1] == 'M':
        return float(x[:-1])*1000000
    else:
        return float(x)

df_new['User votes'] = df_new['User votes'].apply(modify_user_votes)
df_new.head()


# In[16]:


df_new.info()


# ## Label encoding for genre:

# In[17]:


df_new['Genre'] = df_new['Genre'].str.strip("[]").str.replace("'","")


# In[18]:


all_genres = [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 
    'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 
    'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
]


# In[19]:


df_encoded = df_new['Genre'].str.get_dummies(sep=',')
for genre in all_genres:
    if genre not in df_encoded.columns:
        df_encoded[genre] = 0
df_encoded = df_encoded[all_genres]
df_encoded


# In[20]:


df_final = pd.concat([df_new, df_encoded], axis=1, ignore_index=False)
df_final.head()


# In[23]:


## Saving to a csv:
df_final.to_csv("./Filtered_data.csv")


# In[22]:


## Required Dataframe for model:
df = df_final.drop(['Release year','Genre','Duration','Viewership Certificate','Plot synopsis','Director','Poster Link'],axis=1)
df.head()


# In[ ]:




