import requests
from bs4 import BeautifulSoup

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
  
def get_article_text(content, site):
    match site:
        case 'express':
          body = content.find('div', id="article-body")
          paragraphs = body.find_all('p')
          return paragraphs
        case 'guardian':
          paragraphs = content.find_all('p', class_="bodytext")
          return paragraphs
        case 'newsday':
          body = body = content.find('article', class_="article-content")
          paragraphs = body.find_all('p')
          return paragraphs
