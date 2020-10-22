# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 11:24:36 2020

@author: bmano
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import collections


os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

SCOPE = "playlist-modify-public,playlist-modify-private"
CACHE = ".cache-" + "test"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE,
                                                client_id='899c7be4628e42ebba1718d33d2fda4f', 
                                                client_secret='07d5f0b433cb465095df45c729a950ea',
                                                cache_path=CACHE))
playlists_csv = "UserPlaylists.csv"
#read user_ids and emails from user_csv
df = pd.read_csv(playlists_csv)
link_df = collections.defaultdict(list)
for week_num in range(1,7):
    playlists = {df['user_id'][x] : df[str(week_num)][x] for x in range(len(df['user_id'].values.tolist()))}
    
    users = playlists.keys()
    #for each user, create Spotify playlist
    for user_id in users:
        tracks = playlists[user_id].split(";")
        playlist = sp.user_playlist_create(sp.me()['id'], user_id+'_Week'+str(week_num))
        sp.playlist_add_items(playlist['uri'],tracks)
        link_df[user_id].append(playlist['external_urls']['spotify'])
data = pd.DataFrame.from_dict(link_df, orient='index', columns = ['1','2','3','4','5','6'])
data.to_csv(r'PlaylistLinks.csv', header=True)

        