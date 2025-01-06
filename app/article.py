class Article:
  def __init__(self, base_url: str, headline: str, url: str, img_url: str = None):
    self.__base_url = base_url
    self.__headline = headline
    self.__url = url
    self.__img_url = img_url

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
      'img_url' : self.__img_url
    }