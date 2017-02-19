# MI-DDW: Website for experiments with crawlers

  * Implemented in Node.js
  * Randomly generated places/cities and persons that are associated to those cities
  * Two main structures: list of cities/persons and details about each person

## Installation

```bash
git clone https://gitlab.fit.cvut.cz/kuchajar/ddw-crawling-web.git
cd ddw-crawling-web
npm install 
# npm install chance express express-throttle underscore
node index.js
```

## Description

Requirements:
  * User-agent: DDW
  * Throttling: 1 request / second
  * Robots.txt 

Lists:
```html

<h3>Persons:</h3>
<ul class="persons">
    <li><a href="/person/Ronald Collier">Ronald Collier</a></li>
    <li><a href="/person/Marcus Hansen">Marcus Hansen</a></li>
    <li><a href="/person/Franklin Moody">Franklin Moody</a></li>
    ...
</ul>

<h3>Cities:</h3>
<ul class="cities">
    <li><a href="/city/Gusuvjol">Gusuvjol</a></li>
    <li><a href="/city/Femjavun">Femjavun</a></li>
    <li><a href="/city/Mufnijo">Mufnijo</a></li>
    ...
</ul>
```

Person details:
```html
<div class="person">
    <span class="name">Marcus Hansen</span><br />
    <span class="phone">(952) 575-4544</span><br />
    <span class="gender">Female</span><br />
    <span class="age">44</span><br /></div>
</code>
```