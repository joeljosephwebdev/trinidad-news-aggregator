from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin, urlsplit
import json

from helpers import get_html, get_article_text, get_article_img, get_article_date, convert_unicode_to_html_entities
from article import Article
from logger import logging
from constants import ARTICLE_LIST_FILE


def extract_articles(base_url, html_content):
    
    # Generic article extractor that looks for common headline patterns
    # Args:
    #     html_content: String of HTML content
    #     base_url: Base URL for converting relative URLs to absolute
    # Returns:
    #     List of dicts containing headline and URL
    
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    
    # Common headline patterns
    headline_selectors = [
        'h1.headline', 'h2.headline', 'h3.headline', 'h4.headline',
        '.tnt-headline a', '.card-headline a', '.article-title',
        'a[aria-label]', 'h1', 'h2', 'h3', 'h4'
    ]
    
    # Find all potential article elements
    for selector in headline_selectors:
        elements = soup.select(selector)
        for element in elements:
            # Get headline text
            headline = convert_unicode_to_html_entities(element.get_text().strip())
            
            # Skip if too short or looks like navigation
            if len(headline) < 10 or any(word in headline.lower() for word in ['menu', 'navigation', 'search']):
                continue
                
            # Get URL
            if element.name == 'a':
                url = element.get('href', '')
            else:
                url_element = element.find_parent('a') or element.find('a')
                url = url_element.get('href', '') if url_element else ''
            
            # Skip if too short or looks like navigation
            if len(urlsplit(url).path) < 30:
                continue
            
            # Skip opinion pieces and ads
            if ('/opinion/' in url or '/features/' in url or '/multimedia/' in url):
               continue
            
            # Clean and validate URL
            if url:
                url = urljoin(base_url, url)
                articles.append(Article(
                    base_url,
                    headline,
                    url
                ))
    
    # Remove duplicates while preserving order
    seen = set()
    return [x for x in articles if x.get_article()['url'] not in seen and not seen.add(x.get_article()['url'])]

class ArticleList():
  def __init__(self, articles = [], count = 0):
    self.__articles = articles
    self.__count = count
  
  def print_list(self):
    for article in self.__articles:
      print(article)
      
  def add_article(self, article : Article):
     self.__articles.append(article)
     self.__count += 1
  
  def get_article(self, article_num):
    try:
      article = list(self.__articles)[article_num]
    except:
      raise ValueError("Article not found")
    
    return article
  
  def populate_article_list(self, base_urls):
    for base_url in base_urls:
      logging.info(f"Searching {base_url} for articles...")
      html_content = str(get_html(base_url))
      site_articles = extract_articles(base_url, html_content)

      logging.info(f"{len(site_articles)} articles found...")
      for article in site_articles:
         self.add_article(article)
  
  def pull_article_details(self):
     for article in self.__articles:
        article_details = article.get_article()
        content = get_html(article_details['url'])

        body = get_article_text(content, article_details['base_url'], article_details['url'])
        article.set_text(body)

        publish_date = get_article_date(content, article_details['base_url'], article_details['url'])
        article.set_publish_date(publish_date)

        img_url = get_article_img(content, article_details['base_url'], article_details['url'])
        article.set_img_url(img_url)

  
  def get_length(self):
     return self.__count
  
  def save_list(self):
    logging.info(f"writing list of articles to {ARTICLE_LIST_FILE}...")

    article_json = {}

    try:
      for index, article in enumerate(self.__articles):
        article_json[index] = article.get_article()
    except Exception as e:
       logging.error(f"Error building json data from article list {e}")

    try:
      with open(ARTICLE_LIST_FILE, 'w') as file:
        json.dump(article_json, file, indent=4)
    except Exception as e:
       logging.error(f"Error writing json to file - {e}")
    finally:
       logging.info(f"all articles written successfully!")
    
  

