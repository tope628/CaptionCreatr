#!/usr/bin/python3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import billboard
from bs4 import BeautifulSoup
import random
import requests
import os
from profanityfilter import ProfanityFilter

pf = ProfanityFilter()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.url_map.strict_slashes = False
headers = {'Authorization': 'Bearer eCrneseMwLAhfmD8a2wUuKFHGV7N0ZSRSPUvSsenf5KK1JiYanWiF5xJxy1rTB0p'}
search_url = "http://api.genius.com/search"
db = SQLAlchemy(app)


class Hash(db.Model):
    count = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashtag = db.Column(db.String(80))

    def __init__(self, hashtag):
        self.hashtag = hashtag


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def search():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        if hashtag:
            hashtag = hashtag.split("#")
            hashtag = "".join(hashtag)
            data = {'q': hashtag}
            hash_db = hashtag.split(" ")
            for word in hash_db:
                hashes = Hash(word)
                hashes.hashtag = word
                db.session.add(hashes)
                db.session.commit()
        else:
            return random100()
    r = requests.get(search_url, params=data, headers=headers).json()
    return render_template('lyrics.html', lyrics=print_lyrics(r), song=song_info(r), thumbnail=song_thumbnail(r), url=song_url(r))


@app.route('/random', methods=['POST'])
def random100():
    if request.method == 'POST':
        chart = billboard.ChartData('hot-100')
        song = random.choice(chart)
        data = {'q': song.title}

    r = requests.get(search_url, params=data, headers=headers).json()
    return render_template('lyrics.html', lyrics=print_lyrics(r), song=song_info(r), thumbnail=song_thumbnail(r), url=song_url(r))


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
    lyrics = lyrics.replace('\n', '. ')
    lyrics = pf.censor(lyrics)
    return lyrics[:150]


def song_info(r):
    for hit in r["response"]["hits"]:
        song = hit["result"]["full_title"]
        break
    return song


def song_url(r):
    for hit in r["response"]["hits"]:
        url = hit["result"]["url"]
        break
    return url


def song_thumbnail(r):
    for hit in r["response"]["hits"]:
        thumbnail = hit["result"]["header_image_thumbnail_url"]
        break
    return thumbnail


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
