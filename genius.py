#!/usr/bin/python3

from flask import Flask, render_template, request
from pprint import pprint
import billboard
from bs4 import BeautifulSoup
import random
import requests
from sys import argv

app = Flask(__name__)
headers = {'Authorization': 'Bearer eCrneseMwLAhfmD8a2wUuKFHGV7N0ZSRSPUvSsenf5KK1JiYanWiF5xJxy1rTB0p'}
search_url = "http://api.genius.com/search"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        data = {'q': hashtag}
    r = requests.get(search_url, params=data, headers=headers).json()
    for hit in r["response"]["hits"]:
            lyrics_path = hit["result"]["api_path"]
            break
    return render_template('lyrics.html', lyrics=print_lyrics(lyrics_path))


@app.route('/random100', methods=['GET', 'POST'])
def random100():
    chart = billboard.ChartData('hot-100')
    song = random.choice(chart)
    data = {'q': song.title}

    r = requests.get(search_url, params=data, headers=headers).json()
    for hit in r["response"]["hits"]:
            lyrics_path = hit["result"]["api_path"]
            break
    return render_template('lyrics.html', lyrics=print_lyrics(lyrics_path))


def print_lyrics(lyrics_path):
    song_url = "http://api.genius.com" + lyrics_path
    r = requests.get(song_url, headers=headers).json()
    path = r["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics = str(html.find("div", class_="lyrics").text)
    lyrics = lyrics.replace('\n', '')
    return lyrics[:150]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

