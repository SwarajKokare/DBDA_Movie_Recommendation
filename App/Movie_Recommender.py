#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np


# In[4]:


# Load the dataset
filtered_movies = pd.read_csv("Filtered_data.csv")
filtered_movies


# In[5]:


filtered_movies.rename(columns={
    'Release year': 'Release_year',
    'User votes': 'User_votes',
    'Plot synopsis': 'Plot_synopsis',
    'Poster Link': 'Poster_Link'
}, inplace=True)


# In[6]:


filtered_movies.columns


# In[7]:


movie_nlp = filtered_movies[['Title','Release_year','Genre','Duration','Rating','User_votes','Plot_synopsis','Director','Poster_Link']]
movie_nlp.to_csv("sql_data.csv")


# In[8]:


movie_nlp['combined_features'] = movie_nlp['Title'] + ' ' + movie_nlp['Plot_synopsis'] + ' ' + movie_nlp['Genre'] + ' ' + ' ' + movie_nlp['Genre'] + ' '+ ' ' + movie_nlp['Genre'] + ' ' + movie_nlp['Director']


# In[9]:


# Vectorize combined features using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movie_nlp['combined_features'])


# In[10]:


# Convert to sparse matrix (csr_matrix)
tfidf_matrix_sparse = csr_matrix(tfidf_matrix)


# In[11]:


import pickle
with open ("model.pkl","wb") as file:
    pickle.dump((tfidf_matrix_sparse, tfidf, movie_nlp), file)


# In[12]:


# # Compute cosine similarity
# cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
# cosine_sim


# In[13]:


def get_recommendations(title, min_rating=0):

    # Check if the movie title exists
    if title not in movie_nlp['Title'].values:
        return "Movie not found in the database."

    # Get the index of the movie that matches the title
    idx = movie_nlp[movie_nlp['Title'] == title].index[0]

    # Get the pairwise similarity scores of all movies with that movie on-the-fly
    sim_scores = cosine_similarity(tfidf_matrix_sparse[idx], tfidf_matrix_sparse).flatten()

    # Sort the movies based on similarity scores
    sim_scores_indices = np.argsort(sim_scores)[::-1]

    # Get the scores of the 15 most similar movies
    sim_scores_indices = sim_scores_indices[1:16]

    # Filter movies based on the minimum rating
    similar_movies = movie_nlp.iloc[sim_scores_indices]
    similar_movies = similar_movies[similar_movies['Rating'] >= min_rating]

    # Return the titles of the top recommendations
    return similar_movies[['Title','Rating','Genre','Director','User_votes','Plot_synopsis','Duration','Release_year','Poster_Link']]


# In[14]:


# Example usage
recommended_movies = (get_recommendations('The Avengers', min_rating=2))
print(recommended_movies)


# In[15]:


for index, row in recommended_movies.iterrows():
    print(row["Title"], row["Genre"])


# In[ ]:




