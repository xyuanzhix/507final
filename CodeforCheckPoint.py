import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

CACHE_FILENAME = "cache.json"

CLIENT_ID = 'aab31bf00a434cd8b9c81e1bd4296cad'
CLIENT_SECRET = '982273bd74c94b1da29111cc561312e5'

AUTH_URL = 'https://accounts.spotify.com/api/token'
# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

SPOTIFY_BASE = 'https://api.spotify.com/v1/'

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


class SpotifyAPI:
    def __init__(self, name= None, artist_url= None,
                 top_tracks = [], top_albums= [], 
                 similar= {}, playlists= {}, 
                 top_tags= [], top_songs_by_tag = []):
        client_id = CLIENT_ID
        client_secret = CLIENT_SECRET

    def getTrackID(playlist_id):
        id = []
        play_list = sp.playlist(playlist_id)
        for item in play_list['tracks']['items']:
            track = item['track']
            id.append(track['id'])
        return id

    def getartistid(id):
        meta = sp.track(id)
        artist_id = meta['album']['artists'][0]['id']
        id = [artist_id]
        return id

def make_url_request_using_cache(url, cache, search_header=None):
    ''' checkes if the information is in cache
    Parameters
    ----------
    url: str
        the url of the request being made
    cache: json
        the json file to search and see if url call has been made previously
    Returns
    -------
    None
    '''    
    if (url in cache.keys()):         
        print("Using cache")        
        return cache[url]   
    else:
        if search_header:
            print("Fetching")        
            time.sleep(1)        
            response = requests.get(url, headers=headers)        
            cache[url] = response.json()        
            save_cache(cache)        
            return cache[url]
        else:
            print("Fetching")        
            time.sleep(1)        
            response = requests.get(url)        
            cache[url] = response.json()        
            save_cache(cache)        
            return cache[url]




#if __name__ == '__main__':
