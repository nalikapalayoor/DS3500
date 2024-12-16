
import requests
from bs4 import BeautifulSoup
import os

def save_lyrics_from_url(url, filename, folder):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics_divs = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')
    lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{filename}.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(lyrics)

    return file_path


ctrl_songs = [
    {"url": "https://genius.com/Sza-supermodel-lyrics", "filename": "supermodel"},
    {"url": "https://genius.com/Sza-drew-barrymore-lyrics", "filename": "drew_barrymore"},
    {"url": "https://genius.com/Sza-the-weekend-lyrics", "filename": "the_weekend"},
    {"url": "https://genius.com/Sza-love-galore-lyrics", "filename": "love_galore"},
    {"url": "https://genius.com/Sza-20-something-lyrics", "filename": "20_something"},
]

sos_songs = [

    {"url": "https://genius.com/Sza-blind-lyrics", "filename": "blind"},
    {"url": "https://genius.com/Sza-seek-and-destroy-lyrics", "filename": "seek_and_destroy"},
    {"url": "https://genius.com/Sza-used-lyrics", "filename": "used"},
    {"url": "https://genius.com/Sza-special-lyrics", "filename": "special"},
    {"url": "https://genius.com/Sza-ghost-in-the-machine-lyrics", "filename": "ghost_in_the_machine"},
]

for song in ctrl_songs:
    result = save_lyrics_from_url(song['url'], song['filename'],'data/ctrl')
    print(result)

for song in sos_songs:
    result = save_lyrics_from_url(song['url'], song['filename'],'data/sos')
    print(result)


