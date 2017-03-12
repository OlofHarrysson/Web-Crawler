import requests
from bs4 import BeautifulSoup
import sys
import time
import json

class Person:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


    def __str__(self):
        return "{:s} has a rating of ".format(self.name, self.rating)

def crawler(seed):
    frontier=[seed]
    crawled=[]
    movies = []

    while frontier:
        page=frontier.pop()
        try:
            time.sleep(0.2)
            print('Crawled:'+page)
            headers = {
                'User-Agent': 'DDW School Prague CVUT'
            }

            source = requests.get(page, headers=headers).text
            soup = BeautifulSoup(source, "html5lib")


            person_div = soup.find("div", { "id" : "rec_item" }).findAll("a", href=True)
            print(person_div)
            sys.exit(1)

            if person_div:
                title = soup.find("div", { "class" : "originalTitle" }).contents[0]
                rating = soup.find(itemprop="ratingValue").getText()


                movie = Movie(name, rating)
                movies.append(movie)


            links=soup.findAll('a',href=True)

            crawled.append(page)

            for link in links:
                abs_path = seed + link['href']

                if abs_path not in crawled:
                    frontier.append(abs_path)

        except Exception as e:
            print(e)
    return movies

movies = crawler('http://www.imdb.com/title/tt0482571/?ref_=nv_sr_1') # Movie the Prestige

for movie in movies:
    print(movie)
