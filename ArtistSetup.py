# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 11:24:33 2020

@author: bmano
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
import pandas as pd
import os
import random

os.environ['SPOTIPY_CLIENT_ID'] = 'b2ba77753a6b4c4eabfb48b0f91addd1'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'd9665a2a652a4da1a7b8f14d29febfc2'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

artist_file = "Artists.xlsx"
genres = ["Rock","Pop","Hip-HopR&B"]
#read csv with artist/song list for each genre
data = pd.ExcelFile(artist_file)
#get dataframes for each genre
artist_dfs = [pd.read_excel(data,genre) for genre in genres]
writer = pd.ExcelWriter('ArtistTracks.xlsx', engine='xlsxwriter')
for x in range(len(genres)):
    artist_tracks = {}
    for artist in [y[0] for y in artist_dfs[x].values.tolist()]:
        results = sp.artist_top_tracks('spotify:artist:'+artist)['tracks']
        random.shuffle(results)
        tracks = []
        for track in results:
            #any exclusion criteria?
            #skip songs with remix in title
            if 'REMIX' in track['name'].upper():
                continue
            tracks.append(track['id'])
            if len(tracks) == 3:
                break
        artist_tracks[artist] = ";".join(tracks)
    
    df = pd.DataFrame(list(artist_tracks.items()),columns=['Artist','Tracks'])
    df.to_excel(writer, sheet_name = genres[x])
writer.save()

