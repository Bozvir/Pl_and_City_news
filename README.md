News Scraper Bot

A Python-based web scraper that collects local and national news from Onet.pl and sends them to a Telegram channel. This bot uses Selenium and BeautifulSoup for web scraping and Telegram API for sending notifications. It ensures no duplicate entries by maintaining a list of already processed items.


Features:

Scrapes local and national news from Onet.pl

Sends notifications with images, titles, and links to Telegram

Avoids duplicate entries by checking against a saved list

Runs periodically with adjustable intervals


Requirements:

-Python 3.x

-Selenium

-BeautifulSoup

-Requests

-WebDriver (ChromeDriver)

-Telegram API token


Usage:

Once the setup is complete, run the script, and the bot will start scraping news and sending notifications to your Telegram channel.

The bot scrapes both local (Lodz) and nationwide news from Onet.pl.

The script runs indefinitely, scraping and sending updates every 15 minutes (adjustable).
