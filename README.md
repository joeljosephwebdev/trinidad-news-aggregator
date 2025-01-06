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