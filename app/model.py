import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator
import pyodbc

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://postgres:admin@localhost/food_for_all'

conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 08:16:26 2021

@author: girig
"""



# creating the dataframes for ratings and restaurants
'''df = pd.read_csv("Documents/rating_final.csv")
restaurant = pd.read_csv("Documents/restaurant.csv")
#setting the dimension of the output 
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)'''
#conn_str = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=os.environ.get('DATABASE_URL'); DATABASE=TutorialDB;UID=<username>;PWD=<password>)

query_str = 'SELECT UserID, Cuisine, Day, Rentalcount, Weekday, Holiday, Snow FROM dbo.rental_data'

df = pandas.read_sql(sql=query_str, con=conn_str)

print("Data frame:", df)

# Get all the columns from the dataframe.
columns = df.columns.tolist()

# Filter the columns to remove ones we don't want to use in the training
columns = [c for c in columns if c not in ["Year"]]
 
table = df.pivot_table('rating', ['userID'], 'cuisine')
#row mean of rows
row_mean = table.mean(axis = 1)
#subtracting row mean from the row
n = table.sub(row_mean, axis = 0)
#null values are given 0 values
new_table = n.fillna(0)
#asks users for their ID and validated the ID
def ask_user_ID(): 
    while True:        
        user = input("Please enter your user ID: ")
        if user not in new_table.index:
            print("Please enter a valid user ID")
        else:            
            return user
    return user 

def similar_users(table, user_id,  k):
    # creating a dataframe of just the current user
    user = table[table.index == user_id]    
    # and a dataframe of all other users
    other_users = table[table.index != user_id]  
    # calc cosine similarity between user and each other user
    similarities = cosine_similarity(user,other_users)[0].tolist()
    # create list of userIDs of these users
    indices = other_users.index.tolist()
    # create key/values pairs of user index and their similarity
    index_similarity = dict(zip(indices, similarities))   
    # sort by similarity
    index_similarity_sorted = sorted(index_similarity.items(), key=operator.itemgetter(1))
    index_similarity_sorted.reverse()
    
    # grab k users off the top
    top_users_similarities = index_similarity_sorted[:k]
    users = [u[0] for u in top_users_similarities]
    return users

def recommend_item(user_index, users, matrix, items=5):
    
    # load vectors for similar users
    similar_users = matrix[matrix.index.isin(users)]   
    # calc avg ratings across the 3 similar users
    similar_users = similar_users.mean(axis=0)    
    # convert to dataframe so its easy to sort and filter
    similar_users_df = pd.DataFrame(similar_users, columns=['mean'])        
    # load vector for the current user
    user_df = matrix[matrix.index == user_index]
    # transpose it so its easier to filter
    user_df_transposed = user_df.transpose()
    # rename the column as 'rating'
    user_df_transposed.columns = ['rating']
    # remove any rows without a 0 value. Restaurants not rated yet
    user_df_transposed = user_df_transposed[user_df_transposed['rating']==0]
    # generate a list of restaurants the user has not visited
    restaurant_not_visited = user_df_transposed.index.tolist()   
    # filter avg ratings of similar users for only those restaurants the current user has not visited
    similar_users_df_filtered = similar_users_df[similar_users_df.index.isin(restaurant_not_visited)]
    # order the dataframe
    similar_users_df_ordered = similar_users_df_filtered.sort_values(by=['mean'], ascending=False)
    # grab the top restaurants
    top_n_restaurant = similar_users_df_ordered.head(items)
    top_n_restaurant_indices = top_n_restaurant.index.tolist()
    # lookup these restaurants in the other dataframe to find information about restaurant
    restaurant_information = restaurant[restaurant['cuisine'].isin(top_n_restaurant_indices)]   
    return restaurant_information #restaurants
#ask for user ID
user = ask_user_ID()
#get most similar users
other_users = similar_users(new_table,user, 6)
#get the recommendations
restaurants_recommended = recommend_item(user, other_users, new_table)
#remove placeID column
del restaurants_recommended['cuisine']
#drop the index of csv file
restaurants_recommended.reset_index(drop=True, inplace=True)
print("Recommendations for you!")
#print result
print(restaurants_recommended)
