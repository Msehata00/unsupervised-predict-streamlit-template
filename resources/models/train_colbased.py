"""

    Single Value Decomposition plus plus (SVDpp) model training.

    Author: Explore Data Science Academy.

    Description: Simple script to train and save an instance of the
    SVDpp algorithm on MovieLens data.

"""
import pickle


# Script dependencies
import pandas as pd
import surprise
from surprise import SVD


# Importing datasets
ratings = pd.read_csv('ratings.csv')
ratings.drop('timestamp',axis=1,inplace=True)

import streamlit as st

# Using the script_run_ctx context manager
with st.script_run_ctx():
    # Access information about the running script
    app_mode = st.script_request_queue.RerunData.Mode
    command_line_args = st.script_request_queue.get_request_nowait()

# Use the obtained information as needed
st.write("App Mode:", app_mode)
st.write("Command Line Args:", command_line_args)


def svd_pp(save_path):
    # Check the range of the rating
    min_rat = ratings['rating'].min()
    max_rat = ratings['rating'].max()
    # Changing ratings to their standard form
    reader = surprise.Reader(rating_scale=(min_rat, max_rat))
    # Loading the data frame using surprise
    data_load = surprise.Dataset.load_from_df(ratings, reader)
    # Instantiating surprise
    method = SVD(n_factors=200, lr_all=0.005, reg_all=0.02, n_epochs=40, init_std_dev=0.05)
    # Loading a trainset into the model
    model = method.fit(data_load.build_full_trainset())
    print(f"Training completed. Saving model to: {save_path}")

    return pickle.dump(model, open(save_path, 'wb'))


if __name__ == '__main__':
    svd_pp('SVD.pkl')
