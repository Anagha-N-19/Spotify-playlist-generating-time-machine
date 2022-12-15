import requests
#import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

date = input("Enter YYYY-MM-DD for mixtape: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
client_id = "*********"
client_secret = "*********"
response = requests.get(URL)
web_pg = response.text
soup = BeautifulSoup(web_pg, 'html.parser')
song_list = []
name_req = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
for name in name_req:
    print(name.getText().strip("\n\t"))
    song_list.append(name.getText().strip("\n\t"))

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)
song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]

    except IndexError:
        print(f"{song} not in Spotify")
    else:
        song_uris.append(uri)

playlists = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100.",public = False)
sp.playlist_add_items(playlist_id=playlists["id"], items=song_uris)
print(playlists["external_urls"]["spotify"])