import scraper
import sys
import os


if __name__ == "__main__":
    force = False
    pause = False
    minute = '00'
    hours = ['08', '12', '16', '20']
    if len(sys.argv) > 1:
        if sys.argv[1] == '-f':
            force = True
        elif sys.argv[1] == '-p':
            pause = True
        elif sys.argv[1] == '-fp':
            pause = True
            force = True
        if len(sys.argv) > 2:
            minute = sys.argv[2]

    scraper.scrape(force, pause, minute, hours)
