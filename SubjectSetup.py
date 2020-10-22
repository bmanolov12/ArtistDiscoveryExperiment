# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 12:50:41 2020

@author: bmano
"""

import pandas as pd
from pathlib import Path
import random


artist_excel = "ArtistTracks.xlsx"
user_csv = "UserPrefs.csv"
genres=["Rock","Pop","Hip-HopR&B"]
#read csv with user names and genre preference(s)

#generate playlist of songs for each week for each user
#separate songs in playlist with semicolon, playlists with comma

#write all playlists to csv


#make separate script for reading csv, taking in week number as input, generating all playlists

#read csv with artist/song list for each genre
data = pd.ExcelFile(artist_excel)
#get dataframes for each genre
artist_dfs = [pd.read_excel(data,genre) for genre in genres]
#read artist : tracks into dictionaries
artist_dicts = [{df['Artist'][x] : df['Tracks'][x].split(';') for x in range(len(df['Artist'].values.tolist()))} for df in artist_dfs]

user_df = pd.read_csv(user_csv)
#user id : preferred genres list
#user_id, email, genre
user_ids = {user_df['user_id'][x] : user_df['genre'][x] for x in range(len(user_df['user_id'].values.tolist()))}
#build all playlists for each user
user_playlists = {}
user_artists = {}
for user in user_ids.keys():
    #initialize artist list for user, [singles,multiples]
    user_artists[user] = [[],[]]
    genre_index = genres.index(user_ids[user])
    artistList = list(artist_dicts[genre_index].keys())
    #randomize artist list for each listener so different artists are selected as single/multiple
    random.shuffle(artistList)
    tracks = []
    #shuffle tracks for each artist
    for artist in artistList:
        tmp = artist_dicts[genre_index][artist]
        random.shuffle(tmp)
        tracks.append(tmp)
    playlists = []
    for x in range(6):
        mode = x%2
        #first 10 artists in weeks 1, 3, 5; second 10 in 2,4,6
        tmp_artists = artistList[mode*10:(mode+1)*10]
        #assign each artist as single or multiple
        count = 0
        playlist = []
        for artist in tmp_artists:
            #every other artist is assigned multiple songs to be heard once
            if count % 2 == 1:
                #multiple
                playlist.append('spotify:track:'+tracks[count+(10*mode)][int(x/2)])
            else:
                #single
                playlist.append('spotify:track:'+tracks[count+(10*mode)][0])
            #only add artists on the first and 4th weeks
            if x <= 1:
                user_artists[user][count%2].append(artist)
            count += 1
        #randomize playlist order
        random.shuffle(playlist)
        playlists.append(playlist)
    #add list of 6 playlists to main dictionary
    user_playlists[user] = playlists
#write playlists to csv file
with open("UserPlaylists.csv", "w+") as f:
    f.write("user_id,1,2,3,4,5,6,single_artists,multiple_artists\n")
    for key in user_playlists.keys():
        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(key, ";".join(user_playlists[key][0]),
                                        ";".join(user_playlists[key][1]),
                                        ";".join(user_playlists[key][2]),
                                        ";".join(user_playlists[key][3]),
                                        ";".join(user_playlists[key][4]),
                                        ";".join(user_playlists[key][5]),
                                        ";".join(user_artists[key][0]),
                                        ";".join(user_artists[key][1])))
