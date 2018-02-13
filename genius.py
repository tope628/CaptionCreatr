#!/usr/bin/python3

from flask import Flask, render_template, request
from pprint import pprint
import billboard
from bs4 import BeautifulSoup
import random
import requests
from sys import argv

app = Flask(__name__)
app.url_map.strict_slashes = False
headers = {'Authorization': 'Bearer eCrneseMwLAhfmD8a2wUuKFHGV7N0ZSRSPUvSsenf5KK1JiYanWiF5xJxy1rTB0p'}
search_url = "http://api.genius.com/search"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def search():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        if hashtag:
            data = {'q': hashtag}
        else:
            return random100()
    r = requests.get(search_url, params=data, headers=headers).json()
    return render_template('lyrics.html', lyrics=print_lyrics(r))


@app.route('/random', methods=['POST'])
def random100():
    if request.method == 'POST':
        chart = billboard.ChartData('hot-100')
        song = random.choice(chart)
        data = {'q': song.title}

    r = requests.get(search_url, params=data, headers=headers).json()
    return render_template('lyrics.html', lyrics=print_lyrics(r))


def print_lyrics(r):
    for hit in r["response"]["hits"]:
        lyrics_path = hit["result"]["api_path"]
        break

    song_url = "http://api.genius.com" + lyrics_path
    r = requests.get(song_url, headers=headers).json()
    path = r["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics = str(html.find("div", class_="lyrics").text)
    lyrics = lyrics.replace('\n', ' ')
    return lyrics[:150]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

