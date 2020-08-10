import markovify
import os


# This reads from the given subject's headline and fake headline files to create new fake headlines.
def fake_headline(subject):
    my_path = os.path.abspath(os.path.dirname(__file__))
    subject_read = []
    with open(f'{my_path}/hl/{subject}.txt') as subject_txt:
        for entry in subject_txt.readlines():
            subject_read.append(entry.strip())
    fake_read = []
    with open(f'{my_path}/fake_hl/{subject}.txt') as fake_txt:
        for entry in fake_txt.readlines():
            fake_read.append(entry.strip())

    model = markovify.text.Text(subject_read)

    # I've defined subjects and people the bot should not tweet about - I don't think it's in good taste to send
    # a nonsensical headline about a person who has recently passed away.
    # For now this is the only issue that keeps popping up in tweets that I wanted to get rid of, but as for the names
    # it may make sense to update a text file rather than making a list right here in the module.
    illegal_words = ['die', 'dies', 'died', 'death', 'dead', 'assassinate', 'killed']
    illegal_names = ['Nick Cordero', 'Joel Schumacher']

    with open(f'{my_path}/fake_hl/{subject}.txt', 'a') as fake_write:
        for i in range(5):
            do_write = True
            headline = model.make_short_sentence(tries=500, max_chars=200)
            if headline in fake_read or headline in subject_read:
                do_write = False
            for word in illegal_words:
                if word in headline.split():
                    do_write = False
                    break
            for name in illegal_names:
                if name.split()[0] in headline.split() and name.split()[1] in headline.split():
                    do_write = False
                    break
            if do_write:
                fake_write.write(f'{headline}\n')

    print(f'Fake {subject} headlines generated!')


# The Grab Bag produces nonsense headlines from all above areas. Use for maximum absurdity.
def fake_grab_bag():
    illegal_words = ['die', 'dies', 'died', 'death', 'dead', 'assassinate', 'killed']
    illegal_names = ['Nick Cordero', 'Joel Schumacher']
    my_path = os.path.abspath(os.path.dirname(__file__))
    subjects = ['sports', 'entertainment', 'politics', 'tech']
    total_read = []
    total_fake = []
    for subject in subjects:
        with open(f'{my_path}/hl/{subject}.txt') as subject_txt:
            for entry in subject_txt.readlines():
                total_read.append(entry.strip())
    with open(f'{my_path}/fake_hl/grab_bag.txt') as fake_txt:
        for entry in fake_txt.readlines():
            total_fake.append(entry.strip())

    model = markovify.text.Text(total_read)
    with open(f'{my_path}/fake_hl/grab_bag.txt', 'a') as fake_write:
        for i in range(5):
            headline = model.make_short_sentence(tries=100, max_chars=200)
            if headline not in total_fake and headline not in total_read:
                fake_write.write(f'{headline}\n')
    print('Grab bag headlines generated!')


# This is a simple function to use in scraper.py module to update all txt files.
def update_fakes():
    fake_headline('sports')
    fake_headline('entertainment')
    fake_headline('politics')
    fake_headline('tech')
    fake_grab_bag()