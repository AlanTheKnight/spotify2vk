from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
import json
import toml
import colorama


if not os.path.isfile("config.toml"):
    print(colorama.Fore.RED + "Конфигурационный файл (config.toml) не найден")
    exit(0)

if not os.path.isfile("my-songs.json"):
    print(colorama.Fore.RED + "Файл с треками (my-songs.json) не найден")
    exit(0)

with open('config.toml', "r") as f:
    config = toml.load(f)

with open("my-songs.json", "r") as f:
    PLAYLISTS = json.load(f)


USER_AGENT = config["vk"]["user_agent"]
FIREFOX_PROFILE = config["vk"]["firefox_profile"]
AUDIO_URL = config["vk"]["audio_url"]

CREATE_PLAYLIST_BTN = [By.CLASS_NAME, "audio_page__add_playlist_btn"]
COVERS_FOLDER = os.getcwd() + "/covers/"
PLAYLIST_COVER_INPUT = [By.CLASS_NAME, "file"]
PLAYLIST_TITLE_INPUT = [By.ID, "ape_pl_name"]
PLAYLIST_DESCRIPTION_INPUT = [By.ID, "ape_pl_description"]
PLAYLIST_PRIVATE_CHECKBOX = [By.CLASS_NAME, "ape_discover_checkbox"]
PLAYLIST_ADD_SONGS_BTN = [By.ID, "ape_edit_playlist_search"]
SONGS_LIST_HEADER = [By.CLASS_NAME, "ape_list_header"]
NO_SONGS_FOUND = [By.CLASS_NAME, "ape_audios_empty_list"]


options = webdriver.FirefoxOptions()
options.add_argument("user-agent=" + USER_AGENT)
options.add_argument("--profile=" + FIREFOX_PROFILE)
driver = webdriver.Firefox(options=options)

# Open VK
driver.get(AUDIO_URL)

MISSING_SONGS = []

for PLAYLIST in PLAYLISTS:
    el = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(*CREATE_PLAYLIST_BTN).is_displayed())

    # Click on create playlist button
    driver.find_element(*CREATE_PLAYLIST_BTN).click()

    driver.implicitly_wait(2)

    driver.find_element(
        *PLAYLIST_COVER_INPUT).send_keys(COVERS_FOLDER + PLAYLIST["id"] + ".jpg")
    driver.find_element(*PLAYLIST_TITLE_INPUT).send_keys(PLAYLIST["name"])
    driver.find_element(*PLAYLIST_DESCRIPTION_INPUT).send_keys(
        PLAYLIST["description"])
    driver.find_element(*PLAYLIST_PRIVATE_CHECKBOX).click()

    for song in PLAYLIST["songs"]:
        driver.find_element(
            *PLAYLIST_ADD_SONGS_BTN).send_keys(song["artist"] + " - " + song["title"])
        try:
            WebDriverWait(driver, 3).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR, ".ape_list_header").is_displayed()
            )
            driver.find_element(By.CLASS_NAME, "ape_check").click()
        except TimeoutException:
            MISSING_SONGS.append(song["artist"] + "-" + song["title"])
        driver.find_element(By.CLASS_NAME, "ui_search_reset").click()
    driver.find_element(By.CLASS_NAME, "FlatButton").click()

with open("missing-songs.txt", "w") as f:
    for song in MISSING_SONGS:
        f.write(song + "\n")

print(colorama.Fore.GREEN + "Музыка добавлена")
print(colorama.Fore.RED + f"Не найден некоторые треки: {len(MISSING_SONGS)}")
