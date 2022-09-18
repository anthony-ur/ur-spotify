#First pass extract and load, very rough - just landing data (will need to be modularized into extract and load later)

# spotify api wrapper
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# utils
import psycopg2
import json
# creds from env params loader
from src.env import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, DATA_DIR,SPOTIFY_USER_ID


#Authentication - without specific user
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Basic get of full playlists object for user
#TODO: add iteration logic so can handle more than 50 playlist limit
user_playlists = sp.user_playlists(SPOTIFY_USER_ID)
#Save playlists as json to local storage
with open(DATA_DIR + '/playlists.json', 'w') as f:
    json.dump(user_playlists, f)

#Basic get of all tracks for all playlists for a given user
#playlist_tracks = {}
user_playlists_urls = [x["external_urls"] for x in sp.user_playlists(SPOTIFY_USER_ID)["items"]]
for playlist in user_playlists_urls:
    playlist_link = playlist['spotify']
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    playlist_tracks = sp.playlist_tracks(playlist_URI)["items"]
    #Save playlist tracks as json to local storage
    with open(DATA_DIR + '/' + playlist_URI + '_tracks.json', 'w') as f:
        json.dump(playlist_tracks, f)

# Connect to DB
# TODO: externalize all this to main env
conn = psycopg2.connect(
    
    host="host.docker.internal",
    database="postgres",
    user="postgres",
    password="postgres",
    port = 5433)

cur = conn.cursor()

# Create schema and tables
# TODO: move this logic to a db init module, db should prime itself on project start
cur.execute("create schema if not exists raw;")
cur.execute("CREATE TABLE if not exists raw.playlists (id SERIAL PRIMARY KEY, playlist_id VARCHAR, playlist_json JSONB);")
cur.execute("CREATE TABLE if not exists raw.playlist_tracks (id SERIAL PRIMARY KEY, playlist_id VARCHAR, track_id VARCHAR, playlist_track_json JSONB);")
cur.execute("CREATE TABLE if not exists raw.tracks (id SERIAL PRIMARY KEY, track_id VARCHAR, name VARCHAR, track_json JSONB);")
conn.commit()

#Load Playlists Json and insert into DB
with open(DATA_DIR + '/playlists.json') as f:
    playlists = json.load(f)
for playlist in playlists['items']:
    #test_json = '{"collaborative": "False", "description": "", "Items": "test"}'
    actual_test_json = playlist
    insert_sql = "Insert into raw.playlists (playlist_id, playlist_json) values('" + playlist['id'] + "', '" + json.dumps(playlist) +  "');"
    #TODO: need excape char handling if playlist has single quotes
    #print(insert_sql)
    cur.execute(insert_sql)
    conn.commit()
    #print (playlist)

# PLAYLIST_TRACKS
#Grab a list of playlist IDs that we can use to traverse the directory
with open(DATA_DIR + '/playlists.json') as f:
    playlists = json.load(f)
playlist_ids=[x["id"] for x in playlists["items"]]

for playlist_id in playlist_ids:
    #TODO: add handler for file-not-exists
    with open(DATA_DIR + '/' + playlist_id +  '_tracks.json') as f:
        playlist_tracks = json.load(f)
        for playlist_track in playlist_tracks:
            #ugh, string cleaning 
            #TODO: ugh, this is a bad way to do string cleaning like this - need either industrial in-line handler, or build proper own function
            playlist_track['track']['album']['name'] = str((playlist_track['track']['album']['name'])).replace("'",'')
            playlist_track['track']['name'] = str((playlist_track['track']['name'])).replace("'",'')
            playlist_track['track']['artists'] = [str(x["name"]).replace("'",'')  for x in playlist_track['track']['artists']]
            playlist_track['track']['album']['artists'] = [str(x["name"]).replace("'",'')  for x in playlist_track['track']['album']['artists']]
            insert_sql = "Insert into raw.playlist_tracks (playlist_id, track_id, playlist_track_json) values('" + playlist_id + "', '" + playlist_track['track']['id'] + "', '" +  json.dumps(playlist_track) +  "');"
            # print(insert_sql)
            cur.execute(insert_sql)
            conn.commit()

# TRACKS
# from all the playlist tracks loaded, get just a distinct list of tracks
tracks_sql = "select distinct track_id as track_id, playlist_track_json->'track'->>'name' as name from raw.playlist_tracks;" 
cur.execute(tracks_sql)
tracks_result = cur.fetchall()
for track in tracks_result:
    #print(track[0])
    sp.audio_features(track[0])
    insert_sql = "Insert into raw.tracks (track_id, name, track_json) values('" + track[0] + "', '" + track[1] + "', '"  + json.dumps(sp.audio_features(track[0])) +  "');"
    cur.execute(insert_sql)
    conn.commit()


conn.close()