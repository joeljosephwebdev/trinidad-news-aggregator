import requests # type: ignore
import re
import html, unicodedata
import json
from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin, urlsplit

from article import Article
from logger import logging

def get_html(url):
  try:
      # Send a GET request to the URL
      response = requests.get(url)

      # Check if the request was successful
      if response.status_code == 200:
          # Parse the HTML content with BeautifulSoup
          soup = BeautifulSoup(response.text.encode("utf-8"), 'html.parser')

          # Extract the content inside the <body> tag
          body_content = soup.find('body')

          # Return the HTML inside the body, if it exists
          if body_content:
              return body_content # Convert to string to return HTML content
          else:
              logging.error(f"Error: No body tag found in the HTML")
              return
      else:
          logging.error(f"Error: Unable to retrieve content, status code {response.status_code}")
          return

  except requests.exceptions.RequestException as e:
      logging.error(f"Error: An exception occurred - {str(e)}")
      return
  
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
            if ('/opinion/' in url or '/features/' in url or '/multimedia/' in url or '/sponsored/' in url):
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

def convert_unicode_to_html_entities(text):
    result = []
    
    for char in text:
        # Check if the character is not an ASCII character
        if ord(char) > 127:
            # If it's a Unicode character, get its HTML entity
            name = unicodedata.name(char, None)
            if name:
                # Convert it to an HTML entity (named entity or numeric entity)
                result.append(f"&#x{ord(char):X};")  # Hexadecimal representation (e.g., &#x2019;)
            else:
                result.append(html.escape(char))  # For characters without a name, use the generic escape
        else:
            result.append(char)  # If it's an ASCII character, leave it as is
            
    return ''.join(result)

def get_article_text(content, base_url : str, url : str) -> list:
      match base_url:
          case "https://trinidadexpress.com/":
            try: 
              body = content.find('div', id="article-body")
              paragraphs = body.find_all('p')
            except Exception as e:
               logging.error(f"No content found for {url}")
          case "https://www.guardian.co.tt/":
            try:
              paragraphs = content.find_all('p', class_="bodytext")
            except Exception as e:
               logging.error(f"No content found for {url}")
          case "https://newsday.co.tt/category/news/":
            try:
              body = body = content.find('article', class_="article-content")
              paragraphs = body.find_all('p')
            except Exception as e:
               logging.error(f"No content found for {url}")
      
      body_string = ''.join([f'<p>{tag.get_text()}</p>' for tag in paragraphs])
      body_html = convert_unicode_to_html_entities(body_string)
      return body_html
    

def get_article_img(content, base_url : str, url : str):
    match base_url:
      case "https://trinidadexpress.com/":
        photo_card = content.find("div", class_="asset-photo card") # get div with main image
        if photo_card:
          img_url = photo_card.find("img").get("src") # get source for main image
          return img_url
      case "https://www.guardian.co.tt/":
        try:
          carousel_div = content.find('div', class_='nd-carousel-container') # check for image carousel
          if carousel_div: # image carousel found
            main_image = carousel_div.find_all('script')[0].get_text() # get the first image from the carousel
            if main_image:
              json_str = main_image.split('=', 1)[1].strip()  # remove "var gJSONi105_1 = "
              json_str = json_str.rstrip(';\n') # remove \n; from the end
              data = json.loads(json_str) # Parse the JSON
              img_path = data['items'][0]['url'] # store the URL of the first item
          else: # single article image
            main_content = content.find('div', class_=re.compile('.*ag-main-col.*')) 
            img_path = main_content.find("img")["data-aghref"]

          img_url = base_url + img_path.lstrip("/")
          return img_url
        except:
          logging.error(f"Image not found for {url}")
      case "https://newsday.co.tt/category/news/":
        try:
          img = content.find('article', class_='article-content').find('img')
          img_url = img["src"]
          return img_url
        except:
           logging.error(f"Image not found for {url}")
    return "image not found"

def get_article_date(content, base_url : str, url : str):
    match base_url:
      case "https://trinidadexpress.com/":
        publish_date = content.find('time')['datetime'].split('T')[0]
        return publish_date
      case "https://www.guardian.co.tt/":
        publish_date = content.find("span", class_="textelement-publishing date").get_text()
        formatted_date = publish_date[:4] + '-' + publish_date[4:6] + '-' + publish_date[6:]
        return formatted_date
      case "https://newsday.co.tt/category/news/":
        publish_date = content.find('time')['datetime']
        return publish_date
