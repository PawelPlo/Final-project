import requests
from geopy.geocoders import Nominatim
import geocoder
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy()
pliki_w_folderze = os.listdir()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

Nomi_locator = Nominatim(user_agent="My App")

my_location= geocoder.ip('me')

latitude= my_location.geojson['features'][0]['properties']['lat']
longitude = my_location.geojson['features'][0]['properties']['lng']

location = Nomi_locator.reverse(f"{latitude}, {longitude}")
print("Your Current IP location is", location)
print(f"Your Current IP latitude is: {latitude}")
print(f"Your Current IP longitude is: {longitude}")


def get_wikipedia_links_by_coordinates(latitude, longitude, radius=1000):
    api_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "format": "json",
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{latitude}|{longitude}",
        "gsradius": radius,
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        articles = data["query"]["geosearch"]

        article_links = []
        for article in articles:
            title = article["title"]
            page_id = article["pageid"]
            article_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            article_links.append({"title": title, "page_id": page_id, "url": article_url})

        return article_links

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

links = get_wikipedia_links_by_coordinates(latitude, longitude, radius=1000)
link_list = {}
for link in links:
    print(f"Title: {link['title']}")
    title = link['title']
    print(title)
    print(f"Page ID: {link['page_id']}")
    print(f"URL: {link['url']}")
    link_name = str(link['url'])
    print()
    link_list[title] = link_name
    print(link_name)

@app.route("/", methods=['POST', 'GET'])
def Objects():
    context = {
        "link": link_list
            }
    return render_template("example.html", context=context)