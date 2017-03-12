import requests
from bs4 import BeautifulSoup
import sys
import time
import json
import random

class Person:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


    def __str__(self):
        return "{:s} has a rating of ".format(self.name, self.rating)


def found_hitler(crawled):
    print("Found a wiki page that references to Adolf Hitler after crawling {:d} pages".format(len(crawled)))
    sys.exit(1)

def valid_link(link, crawled, root_url):
    is_valid = False
    if link.startswith('/wiki/') and root_url + link not in crawled and ":" not in link:
        is_valid = True
    return is_valid

def get_valid_link(links, crawled, root_url):
    next_link = None
    tries = 0

    while next_link is None or not valid_link(next_link, crawled, root_url):
        next_link = random.choice(links)
        next_link = next_link['href']

        tries += 1
        if tries is 10:
            return None

    return root_url + next_link

def get_page_info(soup):
    title = soup.find("h1", { "id" : "firstHeading" }).contents[0]
    print(title)

    # refs = soup.find("div", { "class" : "reflist" }).findAll("a", href=True)
    # refs = soup.find("h2", { "id" : "References" }).find("div", { "class" : "reflist" }).findAll("a", href=True)
    refs = soup.find({ "id" : "References" })
    # references = [ref.contents[0] for ref in refs]
    # print(references)
    print(refs)
    sys.exit(1)



def crawler(seed, root_url):
    frontier=[seed]
    crawled=[]
    movies = []

    while frontier:
        page=frontier.pop()
        try:
            times_per_second = 10
            time.sleep(1/times_per_second)
            print('Crawled:'+page)
            headers = {
                'User-Agent': 'DDW School Prague CVUT'
            }

            source = requests.get(page, headers=headers).text
            crawled.append(page)
            soup = BeautifulSoup(source, "html5lib")

            get_page_info(soup)

            hitler = soup.find(attrs={"href" : "/wiki/Adolf_Hitler"})
            if hitler:
                found_hitler(crawled)



            links = soup.find("div", { "id" : "mw-content-text" }).find('p').findAll("a", href=True)

            if links:
                nbr_links_to_visit = 2
                for i in range(nbr_links_to_visit):
                    next_link = get_valid_link(links, crawled, root_url)
                    if next_link is None:
                        break
                    frontier.append(next_link)

        except Exception as e:
            print(e)


crawler('https://en.wikipedia.org/wiki/Special:Random', 'https://en.wikipedia.org') # Seed
