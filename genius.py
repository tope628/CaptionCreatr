#!/usr/bin/python3

from flask import Flask, render_template
from pprint import pprint
import billboard
from bs4 import BeautifulSoup
import random
import requests
from sys import argv

app = Flask(__name__)
headers = {'Authorization': 'Bearer eCrneseMwLAhfmD8a2wUuKFHGV7N0ZSRSPUvSsenf5KK1JiYanWiF5xJxy1rTB0p'}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def print_lyrics(lyrics_path):
    song_url = "http://api.genius.com" + lyrics_path
    r = requests.get(song_url, headers=headers).json()
    path = r["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics = html.find("div", class_="lyrics").get_text().encode('ascii', 'ignore')
    lyrics = str(lyrics).replace('\n', ' ')
    return lyrics[:150]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    search_url = "http://api.genius.com/search"
    if len(argv) > 1:
        hashtag = argv[1:]
        data = {'q': hashtag}
    else:
        chart = billboard.ChartData('hot-100')
        song = random.choice(chart)
        data = {'q': song.title}

    r = requests.get(search_url, params=data, headers=headers).json()
    for hit in r["response"]["hits"]:
            lyrics_path = hit["result"]["api_path"]
            break
    pprint(print_lyrics(lyrics_path))
