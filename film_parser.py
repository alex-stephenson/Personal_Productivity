#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 10:25:48 2024

@author: alexstephenson
"""

import os
import re
import requests
import pandas as pd

# Directory path
folder_path = "/Users/alexstephenson/Desktop/TV and Film/Film/General"
foreign_path = "/Users/alexstephenson/Desktop/TV and Film/Film/Foreign"



files = ''
# List all files in the directory
files = os.listdir(folder_path)
foreign_films = os.listdir(foreign_path)

files = files + foreign_films


for i in range(len(files)):
    files[i] = files[i].replace('.', ' ')
    files[i] = files[i].replace("[", "(", 1)
    files[i] = files[i].replace("]", ")", 1)
    


def extract_info(filename):
    # Define a regular expression pattern to match the desired format
    pattern = r'^(.*?)\s*(?:\(|\s)(\d{4})'
    
    # Use regular expression to extract information
    match = re.match(pattern, filename)
    
    if match:
        title = match.group(1)
        year = match.group(2)
        return [title.strip(), year]
    else:
        return None

def process_files(files):
    result = []
    for filename in files:
        info = extract_info(filename)
        if info:
            result.append(info)
    return result


# Process the files
output = process_files(files)



# Define the URL
url = "http://www.omdbapi.com/"

# Your OMDB API key
api_key = "a477e7"

# List of lists containing movie titles and years
movies_info = output

# List to store movie data
movie_data = []

# Query OMDB API for each movie
for movie_title, movie_year in movies_info:
    # Define the parameters
    params = {
        "apikey": api_key,
        "t": movie_title,
        "y": movie_year
    }
    
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Append movie data to the list
        movie_data.append(response.json())
    else:
        print(f"Error: Unable to fetch data for {movie_title} ({movie_year})")
        
    if response.json() == {"Response":"False","Error":"Movie not found!"}:
        print(f"Error: Unable to fetch data for {movie_title} ({movie_year})") 

# Transform movie data into DataFrame
df = pd.DataFrame(movie_data)

#clean data to remove NaNs
df = df[~df['Title'].isnull()]
df.reset_index(inplace = True, drop = True)


df['IMDB Rating'] = ''
for i in range(len(df)):
    df['IMDB Rating'][i] = df['Ratings'][i][0]['Value']


df['Rotten Tomatoes Rating'] = ''
for i in range(len(df)):
    df['Rotten Tomatoes Rating'][i] = df['Ratings'][i][1]['Value']
    
df['Metacritic Rating'] = ''
for i in range(len(df)):
    try:
        df['Metacritic Rating'][i] = df['Ratings'][i][2]['Value']
    except IndexError:
        pass  # Skip the row if the 'Ratings' list doesn't have a third element
        
        
df.to_csv(r'/Users/alexstephenson/Desktop/TV and Film/Film/General/films.csv')


