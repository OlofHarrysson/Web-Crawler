import requests
from bs4 import BeautifulSoup
import sys
import time

class Person:
    def __init__(self, name, phone, gender, age):
        self.name = name
        self.phone = phone
        self.gender = gender
        self.age = age

    def __str__(self):
        return "{:s} has the phone number {:s}. Is a {:s} and {:s} years old".format(
                        self.name, self.phone, self.gender, self.age)

def crawler(seed):
    frontier=[seed]
    crawled=[]
    persons = []

    while frontier:
        page=frontier.pop()
        try:
            time.sleep(0.2)
            print('Crawled:'+page)
            headers = {
                'User-Agent': 'DDW'
            }

            source = requests.get(page, headers=headers).text
            soup=BeautifulSoup(source, "html5lib")
            person_div = soup.find("div", { "class" : "person" })

            if person_div:
                name_span = person_div.find("span", { "class" : "name" })
                name = name_span.contents[0]

                phone_span = person_div.find("span", { "class" : "phone" })
                phone = phone_span.contents[0]

                gender_span = person_div.find("span", { "class" : "gender" })
                gender = gender_span.contents[0]

                age_span = person_div.find("span", { "class" : "age" })
                age = age_span.contents[0]


                person = Person(name, phone, gender, age)
                persons.append(person)


            links=soup.findAll('a',href=True)

            crawled.append(page)

            for link in links:
                abs_path = seed + link['href']

                if abs_path not in crawled:
                    frontier.append(abs_path)

        except Exception as e:
            print(e)
    return persons

# crawler('https://fit.cvut.cz')
persons = crawler('http://localhost:8000')

for person in persons:
    print(person)

print("Persons in list is {:d}".format(len(persons)))
