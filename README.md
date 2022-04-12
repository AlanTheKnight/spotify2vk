# spotify2vk

Script that helps to transfer your Spotify playlists to VK Music

## Dependencies

Install dependencies using [Python Poetry](https://python-poetry.org):

```bash
poetry install
```

## Configuration

Create a file named `config.toml` in the root directory of the project.

```toml
[spotify]
client_id = "..."
client_secret = "..."
scope = "playlist-read-private"

[vk]
audio_url = "..."
firefox_profile = "..."
user_agent = "..."
```

`client_id` & `client_secret` can be found in [Spotify developer dashboard](https://developer.spotify.com/dashboard/).

When creating a new Spotify application in the dashboard, don't forget to add `http://localhost:8888/callback` to "Callback URLs" section in app settings.

`audio_url` is a URL of your main VK Music section page.

`firefox_profile` & `user_agent` values can be found if you open Firefox and type "about:support" in URL bar.

## Usage

To collect your Spotify playlists, run:

```bash
poetry run python spotify.py
```

Then transfer them to VK using:

```bash
poetry run python vk.py
```
