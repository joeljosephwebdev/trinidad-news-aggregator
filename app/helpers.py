import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import html, unicodedata

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
        img_url = None
        return img_url
      case "https://www.guardian.co.tt/":
        img_url = None
        return img_url
      case "https://newsday.co.tt/category/news/":
        img_url = None
        return img_url

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
