import tweepy
import random
from google_images_search import GoogleImagesSearch
import os
from googleapiclient.errors import HttpError


# Logs into Twitter account using API keys and access tokens
def login():
    auth = tweepy.OAuthHandler('secret1', 'secret2')
    auth.set_access_token('secret1',
                          'secret2')
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()
    return api


def grab_headline(subject):
    my_path = os.path.abspath(os.path.dirname(__file__))
    fake_list = []
    with open(f'{my_path}/fake_hl/{subject}.txt', 'r') as fake_read:
        fake_read_list = fake_read.readlines()
        start = len(fake_read_list)-10
        if len(fake_read_list)-10 < 0:
            start = 0
        for entry in fake_read_list[start:]:
            fake_list.append(entry)
    hl_index = random.randint(0, len(fake_list)-1)
    return fake_list[hl_index]


# Using the Google Images Search library and Google Developer app + Custom Search to retrieve first Google img result
def retrieve_image(headline, subject):
    engine = GoogleImagesSearch('secret1', 'secret2')
    parameters = {
        'q': headline,
        'num': 1,
        'safe': 'off',
        'fileType': 'png',
        'imgSize': 'XXLARGE'
        }
    my_path = os.path.abspath(os.path.dirname(__file__))
    my_path += '/img/'
    # Downloads the first img result
    try:
        engine.search(search_params=parameters, path_to_dir=my_path)
        new_path = f'{my_path}{os.listdir(my_path)[0]}'
    except HttpError:
        new_path = 'no image'

    return new_path


def tweet(headline, subject, api):
    if subject == 'grab_bag':
        subject = 'grab bag'
    tweet_msg = f'{subject.upper()}: {headline}'
    media = retrieve_image(headline, subject)
    if media != 'no image':
        ids = []
        with open(media, 'rb') as media_file:
            ids.append(api.media_upload(media, file=media_file).media_id)

        try:
            api.update_status(media_ids=ids, status=tweet_msg)
            print('Tweet sent successfully!')
        except tweepy.error.TweepError:
            print('Could not send tweet!')
        os.remove(media)
        print('Media cleaned!')
    else:
        try:
            api.update_status(status=tweet_msg)
            print('Tweet sent successfully!')
        except tweepy.error.TweepError:
            print('Could not send tweet!')
        print('No media needed to be cleaned.')

