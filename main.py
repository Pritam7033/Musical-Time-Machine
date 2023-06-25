import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


spotify_client_id = Type your client id here
spotify_client_secret = Type your client secret here
URL = "https://www.billboard.com/charts/hot-100/"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri="http://example.com",
        show_dialog=True,
        cache_path="token.txt",
        username="ABHIJIT KUMAR"
    )

)

user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD :")

response = requests.get(url=f"{URL}{date}/")
html_data = response.text

soup = BeautifulSoup(html_data, "html.parser")
song_titles = [item.get_text().strip() for item in soup.select("li h3#title-of-a-story")]
song_uris = []
year = date.split("-")[0]
for song in song_titles:
    print(song)
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
