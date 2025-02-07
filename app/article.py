class Article:
  def __init__(
      self, 
      base_url: str, 
      headline: str, 
      url: str, 
      img_url: str = "./static/images/image_not_found.png", 
      body : str = None,
      publish_date : str = None
      ):
    self.__base_url = base_url
    self.__headline = headline
    self.__url = url
    self.__img_url = img_url
    self.__body = body
    self.__publish_date = publish_date

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
      'article_body' : self.__body,
      'publish_date' : self.__publish_date,
    }
  
  def set_img_url(self, img_url : str):
    if img_url != "image not found":
      self.__img_url = img_url

  def set_text(self, body : str):
    self.__body = body
  
  def set_publish_date(self, publish_date : str):
    self.__publish_date = publish_date
