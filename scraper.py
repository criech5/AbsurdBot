from bs4 import BeautifulSoup
import requests
import markovify
from datetime import datetime
from selenium import webdriver
import headline_faker
import tweeter
import os
import sys


def sports_scraper():
    sports_headlines = []
    # Currently, this method pulls from CBS Sports for its sporting news.
    # Right now, only a few sports are supported. I figure this is probably better for training data than many unrelated
    # headlines but hey, what do I know.
    sites_list = ["https://www.cbssports.com/nfl/",
                  "https://www.cbssports.com/mlb/",
                  "https://www.cbssports.com/nba/",
                  "https://www.cbssports.com/nhl/",
                  "https://www.cbssports.com/soccer/",
                  "https://www.cbssports.com/college-football/",
                  "https://www.cbssports.com/wnba/",
                  "https://www.cbssports.com/college-basketball/",
                  "https://www.cbssports.com/tennis/",
                  "https://www.cbssports.com/golf/"]

    # Each subject scraper follows generally the same process - the main differentiations are in the formatting
    # of each website used. I'll explain the process in this scraper function.
    for site in sites_list:
        # We get the page using a GET request and create a BeautifulSoup object to make it easier to examine.
        page = requests.get(site)
        page_content = page.content
        my_soup = BeautifulSoup(page_content, 'html.parser')

        # h1 tag
        # We append the headlines from each tag given for a site.
        h1s = my_soup.find_all('h1')
        for h1 in h1s:
            sports_headlines.append(h1.get_text().strip())

        # h2 tag
        h2s = my_soup.find_all('h2')
        for h2 in h2s:
            sports_headlines.append(h2.get_text().strip())

        # h3 tag
        h3s = my_soup.find_all('h3')
        for h3 in h3s:
            if h3['class'][0] != 'Newsletter-title':
                sports_headlines.append(h3.get_text().strip())

    return sports_headlines


def entertainment_scraper():
    entertainment_headlines = []
    sites_list = ["https://www.cnn.com/entertainment",
                  "https://www.msn.com/en-us/entertainment"]
    for site in sites_list:
        page = requests.get(site)
        page_content = page.content
        my_soup = BeautifulSoup(page_content, 'html.parser')

        # if site == "https://www.dailymail.co.uk/usshowbiz/index.html":
        #     # h2 tag
        #     h2s = my_soup.find_all('h2')
        #     for h2 in h2s:
        #         entertainment_headlines.append(h2.get_text().strip())

        # if site == "https://www.cnn.com/entertainment":
        # h3 tag
        h3s = my_soup.find_all('h3')
        for h3 in h3s:
            entertainment_headlines.append(h3.get_text().strip())

    return entertainment_headlines


def politics_scraper():
    my_path = os.path.abspath(os.path.dirname(__file__))
    politics_headlines = []
    sites_list = ["https://www.nytimes.com/section/politics",
                  "https://www.cnn.com/politics",
                  "https://www.politico.com/politics"]
    for site in sites_list:
        page = requests.get(site)
        page_content = page.content
        my_soup = BeautifulSoup(page_content, 'html.parser')
        # CNN Politics is a dynamic page, so we have to utilize Selenium to scrape it.
        # This requires having Chromium and its corresponding driver properly installed, and also must be run in
        # headless mode since in production, this will be run in a Docker container.
        if site == "https://www.cnn.com/politics":
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            options.add_argument('--log-level=3')
            options.add_argument('--no-sandbox')
            options.binary_location = "/usr/bin/chromium-browser"
            driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
            driver.get(site)
            page_content = driver.page_source
            my_soup = BeautifulSoup(page_content, 'html.parser')

        if site == "https://www.cnn.com/politics" or site == "https://www.politico.com/politics":
            # h3 tag
            h3s = my_soup.find_all('h3')
            illegal_hls = ['Your Privacy', 'Share my Data with 3rd Parties', 'Strictly Necessary Cookies',
                           'Advertising Cookies', '33Across']
            for h3 in h3s:
                if h3.get_text() not in illegal_hls:
                    politics_headlines.append(h3.get_text().strip())

        elif site == "https://www.nytimes.com/section/politics":
            # h2 tag
            h2s = my_soup.find_all('h2')
            illegal_hls = ['The On Politics Newsletter', 'Highlights', 'Follow Us', 'Site Index',
                           'Site Information Navigation']
            for h2 in h2s:
                if h2.get_text() not in illegal_hls:
                    politics_headlines.append(h2.get_text().strip())

    return politics_headlines


def tech_scraper():
    tech_headlines = []
    sites_list = ["https://www.cnet.com/news/",
                  "https://www.digitaltrends.com/news/"]
    for site in sites_list:
        page = requests.get(site)
        page_content = page.content
        my_soup = BeautifulSoup(page_content, 'html.parser')

        # h3 tag
        h3s = my_soup.find_all('h3')
        for h3 in h3s:
            tech_headlines.append(h3.get_text().strip())
        if site == "https://www.cnet.com/news/":
            h6s = my_soup.find_all('h6')
            for h6 in h6s:
                tech_headlines.append(h6.get_text().strip())

    return tech_headlines

# This function was created to minimize duplicate text in the scrape() function; it runs a particular scraper to
# return a list of headlines and then inserts that list into a subject text file.
def scrape_subject(subject):
    hls = []
    my_path = os.path.abspath(os.path.dirname(__file__))
    if subject == 'sports':
        hls = list(dict.fromkeys(sports_scraper()))
    if subject == 'entertainment':
        hls = list(dict.fromkeys(entertainment_scraper()))
    if subject == 'politics':
        hls = list(dict.fromkeys(politics_scraper()))
    if subject == 'tech':
        hls = list(dict.fromkeys(tech_scraper()))

    txt = []
    with open(f'{my_path}/hl/{subject}.txt', 'r') as txt_raw:
        for entry in txt_raw.readlines():
            txt.append(entry.strip())

    for hl in hls:
        if hl not in txt:
            with open(f'{my_path}/hl/{subject}.txt', 'a', encoding='utf-8') as w:
                w.write(f'{hl}\n')
    # Notify the console
    print(f'{subject.capitalize()} headlines updated!')


def scrape(force=False, pause=False, minute='05', hours=['08','12','16','20']):
    sports_done = False
    ent_done = False
    pol_done = False
    tech_done = False
    exe_done = False
    tweet_done = False

    while True:
        now = datetime.now()
        min_t = datetime.strftime(now, '%M')
        hour = datetime.strftime(now, '%H')

        # Scraping sports sites for new headlines half-hourly

        if min_t == '00' or min_t == '30' or force:
            if not sports_done:
                scrape_subject('sports')
                sports_done = True
        else:
            sports_done = False

        # Scraping entertainment sites for new headlines half-hourly
        if min_t == '01' or min_t == '31'or force:
            if not ent_done:
                scrape_subject('entertainment')
                ent_done = True
        else:
            ent_done = False

        # Scraping politics sites for new headlines half-hourly
        if min_t == '02' or min_t == '32' or force:
            if not pol_done:
                scrape_subject('politics')
                pol_done = True
        else:
            pol_done = False

        # Scraping tech sites for new headlines half-hourly
        if min_t == '03' or min_t == '33' or force:
            if not tech_done:
                scrape_subject('tech')
                tech_done = True
        else:
            tech_done = False

        # Running headline_faker.py to update txt files containing fake headlines
        if min_t == '04' or min_t == '34' or force:
            if not exe_done:
                print('Headlines now being faked!')
                headline_faker.update_fakes()
                exe_done = True
        else:
            exe_done = False

        # Running tweeter.py functions to tweet the generated headlines
        if ((min_t == minute and hour in hours) or force) and not pause:
            if not tweet_done:
                subjects = ['sports', 'entertainment', 'politics', 'tech', 'grab_bag']
                for subject in subjects:
                    api = tweeter.login()
                    headline = tweeter.grab_headline(subject)
                    tweeter.tweet(headline, subject, api)
                tweet_done = True
        else:
            tweet_done = False

