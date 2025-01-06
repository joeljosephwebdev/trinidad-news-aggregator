from helpers import get_html, get_article_text, get_article_img, convert_unicode_to_html_entities

class Article:
  def __init__(self, base_url: str, headline: str, url: str, img_url: str = None, body : str = None):
    self.__base_url = base_url
    self.__headline = headline
    self.__url = url
    self.__img_url = img_url
    self.__body = body

  def __str__(self):
    return f"""{'-' * 40}
Source = {self.__base_url}
Headline = {self.__headline}
Link = {self.__url} 
Image Link = {self.__img_url}
  """.strip()

  def get_article(self):
    return {
      'base_url' : self.__base_url,
      'headline' : self.__headline,
      'url' : self.__url,
      'img_url' : self.__img_url,
      'article_body' : self.__body
    }
  
  def set_img_url(self, img_url : str):
    self.__img_url = img_url

  def set_text(self, body : str):
    self.__body = body
  
  def pull_details(self) -> int:
    content = get_html(self.__url)
    if content :
      body = get_article_text(content, self.__base_url, self.__url)
      body_string = ''.join([f'<p>{tag.get_text()}</p>' for tag in body])
      body_html = convert_unicode_to_html_entities(body_string)
      self.set_text(body_html)
