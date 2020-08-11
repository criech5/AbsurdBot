# AbsurdBot
A Twitter bot which scrapes news websites and generates an absurd headline using Markov chains, then tweets it with a related image.
This code is designed to run for long periods of time using Docker - you can view it in action at https://twitter.com/absurd_bot. (As of 08/11/20, though, it is down for maintenance.)

Libraries promienently featured in this project:

Tweepy - uses Twitter's API to send tweets with and without attached media

BeautifulSoup 4 - streamlines the processing of webpages

Selenium - helps scrape pages which are not "purely HTML"

Markovify - composes a fake headline using the scraped data and Markov chains

GoogleImagesSearch - retrieves a photo related to a generated headline
