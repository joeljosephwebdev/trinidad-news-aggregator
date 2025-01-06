import time

from articlelist import ArticleList
from constants import BASE_URLS
from logger import logging

def main():
  start = time.time()
  logging.info(f"------- Aggregator Initialized -------")
  articles = ArticleList()
  articles.populate_article_list(BASE_URLS)
  logging.info(f"{articles.get_length()} total articles found!")

  logging.info(f"Fetching article details...")
  articles.pull_article_details()
  logging.info(f"Article details complete!")

  logging.info(f"Saving articles to...")
  articles.save_list()
  logging.info(f"{articles.get_length()} articles saved!")
  end = time.time()
  logging.info(f"Aggregation completed in {end - start:.2f}s")

if __name__ == "__main__":
  main()