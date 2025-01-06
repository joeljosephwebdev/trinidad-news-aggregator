# Trinidad News Aggregator 🌏📰🤖

## Authors 🙋‍♂️

- [Joel Joseph](https://www.github.com/joeljosephwebdev)

## Description

This is an automated aggregator for websites covering Trinidad & Tobago news.

## Getting Started 💫

Getting started is easy. Just clone the repo, install the requirements, run the test suite to make sure everything passes, then run the main shell script.

The app will crawl the homepage for each website, build of list of all current article headlines and urls, then save that list to a json file (article_list.json). 

* run app
   ```sh
   ./main.sh

* run test suite
  ```sh
  ./test.sh

### Prerequisites 🚀

For this project, you will need python3, the requests library and beautifulsoup.
To get setup, ensure you have python 3 installed. You can verify the version with:

* python version
   ```sh
    python3 --version  
    Python 3.13.1

Install project requirements:

* requirements
   ```sh
   pip3 install -r requirements.txt


### Example 

```sh
  >> ./main.sh
  2025-01-05 23:14:51,189 - INFO - ------- Aggregator Initialized -------
  2025-01-05 23:14:51,190 - INFO - Searching https://trinidadexpress.com/ for articles...
  2025-01-05 23:14:51,201 - DEBUG - Starting new HTTPS connection (1): trinidadexpress.com:443
  2025-01-05 23:14:51,636 - DEBUG - https://trinidadexpress.com:443 "GET / HTTP/1.1" 200 61654
  2025-01-05 23:14:51,759 - DEBUG - Encoding detection: utf_8 is most likely the one.
  2025-01-05 23:14:51,928 - INFO - 23 articles found...
  2025-01-05 23:14:51,928 - INFO - Searching https://www.guardian.co.tt/ for articles...
  2025-01-05 23:14:51,929 - DEBUG - Starting new HTTPS connection (1): www.guardian.co.tt:443
  2025-01-05 23:14:52,429 - DEBUG - https://www.guardian.co.tt:443 "GET / HTTP/1.1" 200 None
  2025-01-05 23:14:52,559 - INFO - 16 articles found...
  2025-01-05 23:14:52,559 - INFO - Searching https://newsday.co.tt/category/news/ for articles...
  2025-01-05 23:14:52,560 - DEBUG - Starting new HTTPS connection (1): newsday.co.tt:443
  2025-01-05 23:14:53,001 - DEBUG - https://newsday.co.tt:443 "GET /category/news/ HTTP/1.1" 200 14828
  2025-01-05 23:14:53,113 - INFO - 22 articles found...
  2025-01-05 23:14:53,113 - INFO - 61 total articles found!
  2025-01-05 23:14:53,113 - INFO - writing list of articles to article_list.json...
  2025-01-05 23:14:53,115 - INFO - all articles written successfully!
  2025-01-05 23:14:53,115 - INFO - Aggregation completed in 1.93s