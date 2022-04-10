from genericpath import isdir
import json
import os
from functools import reduce
from os.path import isfile, isdir
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import toml
import requests
import colorama


colorama.init(autoreset=True)


if not isfile("config.toml"):
    print(colorama.Fore.RED + "Конфигурационный файл (config.toml) не найден")
    exit(0)

with open('config.toml') as f:
    config = toml.load(f)

if not isdir("covers"):
    print(colorama.Fore.YELLOW + "Добавление папки covers")
    os.mkdir("covers")


auth = SpotifyOAuth(client_id=config['spotify']['client_id'],
                    client_secret=config['spotify']['client_secret'],
                    redirect_uri='http://localhost:8888/callback',
                    scope=config['spotify']['scope'])

spotify = spotipy.Spotify(auth_manager=auth)
print(colorama.Fore.GREEN + "Авторизация в Spotify успешна")


def get_playlists():
    results = spotify.current_user_playlists(limit=50)
    playlists = results['items']
    while results['next']:
        results = spotify.next(results)
        playlists.extend(results['items'])
    return playlists


def get_playlist_songs(uid: str):
    results = spotify.playlist_items(uid)
    songs = list(map(get_song_info, results["items"]))
    while results["next"]:
        results = spotify.next(results)
        songs.extend(list(map(get_song_info, results["items"])))
    return songs


def get_song_info(record: dict):
    song = record["track"]
    return {
        "artist": reduce(lambda a, b: a + ", " + b, (i["name"] for i in song["artists"])),
        "title": song["name"]
    }


if __name__ == '__main__':
    playlists = get_playlists()
    print(colorama.Fore.BLUE + "Ваши плейлисты:")
    for i, playlist in enumerate(playlists):
        print(f"{i+1})", playlist['name'])

    selected = input("Выберите плейлист(ы): ")
    to_transfer = playlists if selected == "all" else list(
        map(lambda x: playlists[int(x) - 1], selected.split()))

    result = []

    for sp in to_transfer:
        image_url = sp["images"][0]["url"]
        with open("covers/" + sp["id"] + ".jpg", "wb") as f:
            f.write(requests.get(image_url).content)

        cur = {
            "name": sp["name"],
            "description": sp["description"],
            "songs": get_playlist_songs(sp["id"]),
            "id": sp["id"]
        }

        print(colorama.Fore.GREEN + f"✅ Плейлист {sp['name']} загружен")
        result.append(cur)

    with open("my-songs.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
