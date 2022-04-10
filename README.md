# spotify2vk

Script that helps to transfer your Spotify playlists to VK Music

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

## Usage

To collect your Spotify playlists, run:

```bash
poetry run python spotify.py
```

To transfer them to VK use:

```bash
poetry run python vk.py
```
