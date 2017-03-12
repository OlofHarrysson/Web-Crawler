import requests
from bs4 import BeautifulSoup
import sys
import time
import json
import random

class Page:
    def __init__(self, url, title, heading, languages):
        self.url = url
        self.title = title
        self.heading = heading
        self.languages = languages
        self.languages.append('English')

    def __str__(self):
        nbr_lang = len(self.languages)
        return "The page has the heading: {:s} \t url: {:s} \t and exists in {:d} languages".format(self.heading, self.url, nbr_lang)

    def print_lang(self):
        lang_str = " ".join([str(x) for x in self.languages])
        print(lang_str)


def finish_prog(crawled, pages):
    print("Found a wiki page that references to Adolf Hitler after crawling {:d} pages".format(len(crawled)))

    pages_dict = dict()
    for page in pages:
        pages_dict[page.heading] = page.__dict__


    with open('pages.json', 'w') as outfile:
        json.dump(pages_dict, outfile)

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
    heading = soup.find("h1", { "id" : "firstHeading" }).contents[0]

    title = soup.find({"title"}).contents[0]

    lang_links = soup.find("div", {"id" : "p-lang"}).find("div", {"class" : "body"}).findAll("a")
    if lang_links:
        languages = [lang_link.contents[0] for lang_link in lang_links]
        languages.pop() # Remove Add/Edit link


    return heading, title, languages


def crawler(seed, root_url):
    frontier=[seed]
    crawled=[]
    pages = []

    while frontier:
        page_url=frontier.pop()
        try:
            times_per_second = 10
            time.sleep(1/times_per_second)
            # print('Crawled:'+page_url)
            headers = {
                'User-Agent': 'DDW School Prague CVUT'
            }

            source = requests.get(page_url, headers=headers).text
            crawled.append(page_url)
            soup = BeautifulSoup(source, "html5lib")

            heading, title, languages = get_page_info(soup)

            page = Page(page_url, title, heading, languages)
            print(page)
            pages.append(page)

            hitler = soup.find(attrs={"href" : "/wiki/Adolf_Hitler"})
            if hitler:
                finish_prog(crawled, pages)


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
