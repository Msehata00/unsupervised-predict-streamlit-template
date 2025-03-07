"""

    Collaborative-based filtering for item recommendation.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: You are required to extend this baseline algorithm to enable more
    efficient and accurate computation of recommendations.

    !! You must not change the name and signature (arguments) of the
    prediction function, `collab_model` !!

    You must however change its contents (i.e. add your own collaborative
    filtering algorithm), as well as altering/adding any other functions
    as part of your improvement.

    ---------------------------------------------------------------------

    Description: Provided within this file is a baseline collaborative
    filtering algorithm for rating predictions on Movie data.

"""



# Script dependencies
import pandas as pd
import numpy as np
import pickle
from comet_ml import Experiment 
import copy
from surprise import Reader, Dataset
from surprise import SVD, NormalPredictor, BaselineOnly, KNNBasic, NMF
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#from ast import literal_eval

import ast
# Importing data
movies_df = pd.read_csv('resources/data/movies.csv',sep = ',')
ratings_df = pd.read_csv('resources/data/ratings.csv')
ratings_df.drop(['timestamp'], axis=1,inplace=True)
#movies_df['genres'] = movies_df['genres'].apply(lambda x: '|'.join(ast.literal_eval(x)))
#movies_df['genres'] = movies_df['genres'].apply(literal_eval).apply(lambda x: [item['name'] for item in x] if isinstance(x, list) else [])
# We make use of an SVD model trained on a subset of the MovieLens 10k dataset.
model_path = 'resources/models/SVD.pkl'
model = pickle.load(open(model_path, 'rb'))


def prediction_item(item_id):
    """Map a given favourite movie to users within the
       MovieLens dataset with the same preference.

    Parameters
    ----------
    item_id : int
        A MovieLens Movie ID.

    Returns
    -------
    list
        User IDs of users with similar high ratings for the given movie.

    """
    # Data preprosessing
    reader = Reader(rating_scale=(0, 5))
    load_df = Dataset.load_from_df(ratings_df,reader)
    a_train = load_df.build_full_trainset()

    predictions = []
    for ui in a_train.all_users():
        predictions.append(model.predict(iid=item_id,uid=ui, verbose = False))
    return predictions

def pred_movies(movie_list):
    """Maps the given favourite movies selected within the app to corresponding
    users within the MovieLens dataset.

    Parameters
    ----------
    movie_list : list
        Three favourite movies selected by the app user.

    Returns
    -------
    list
        User-ID's of users with similar high ratings for each movie.

    """
    # Store the id of users
    id_store=[]
    # For each movie selected by a user of the app,
    # predict a corresponding user within the dataset with the highest rating
    for i in movie_list:
        predictions = prediction_item(item_id = i)
        predictions.sort(key=lambda x: x.est, reverse=True)
        # Take the top 10 user id's from each movie with highest rankings
        for pred in predictions[:10]:
            id_store.append(pred.uid)
    # Return a list of user id's
    return id_store

# !! DO NOT CHANGE THIS FUNCTION SIGNATURE !!
# You are, however, encouraged to change its content.  
def collab_model(movie_list,top_n=10):
    """Performs Collaborative filtering based upon a list of movies supplied
       by the app user.

    Parameters
    ----------
    movie_list : list (str)
        Favorite movies chosen by the app user.
    top_n : type
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """
  
    # Load the pre-trained model
    model = pickle.load(open('resources/models/ALS_model.pkl', 'rb'))

    # Prepare the data for prediction
    movie_ids = pred_movies(movie_list)
    user_id = max(movie_ids) + 1
    user_ratings = [(user_id, movie_id, 0) for movie_id in movie_ids]

    # Get prediction scores for all movies
    predictions = []
    for movie_id in movies_df['movieId'].values:
        predicted_rating = model.predict(user_id, movie_id).est
        predictions.append((movie_id, predicted_rating))

    # Sort predictions in descending order of ratings
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Get top_n recommended movie titles
    recommended_movies = []
    for movie_id, _ in predictions[:top_n]:
        predicted_rating = model.predict(user_id, movie_id).est
        #recommended_movies_with_info.append((movie_title, genres, predicted_rating))
        genres = movies_df[movies_df['movieId'] == movie_id]['genres'].values[0]
        recommended_movies.append((movies_df[movies_df['movieId'] == movie_id]['title'].values[0],genres,predicted_rating))

        
    return recommended_movies


