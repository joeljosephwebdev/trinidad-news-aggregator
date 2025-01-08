import unittest
import sys
import os
import logging
from bs4 import BeautifulSoup #type: ignore

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the directory above
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

logging.disable()

from helpers import get_html, get_article_text, get_article_date, get_article_img, convert_unicode_to_html_entities

class TestGetHtml(unittest.TestCase):
  def test_get_html(self):
    base_url = "https://motherfuckingwebsite.com/"
    html = str(get_html(base_url))
    self.assertTrue("fuck" in html)
  
  def test_get_article_not_found(self):
    with self.assertRaises(Exception) as context:       
      base_url = "https://motherfuckingwebsite.com/does_not_exist"
      html = str(get_html(base_url))
      self.assertTrue("Error: Unable to retrieve content, status code 404" in context)

class TestGetArticleText(unittest.TestCase):
  def test_get_article_text_guardian(self):
    with open('app/tests/sample_guardian_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      article_text = get_article_text(soup, "https://www.guardian.co.tt/", None)
      self.assertIn(str(article_text[0]), '<p class="bodytext">Se­nior Re­porter</p>')
  
  def test_get_article_text_express(self):
    with open('app/tests/sample_express_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      article_text = get_article_text(soup, "https://trinidadexpress.com/", None)
      self.assertIn(str(article_text[0]), "<p>The big question on everyone's mind is: who will replace Prime Minister Dr Keith Rowley?</p>")
  
  def test_get_article_text_newsday(self):
    with open('app/tests/sample_newsday_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      article_text = get_article_text(soup, "https://newsday.co.tt/category/news/", None)
      self.assertIn(str(article_text[0]), "<p>A pallet of Forres Park Puncheon Rum valued at approximately $25,000 has been reported stolen from the Angostura Ltd warehouse.</p>")

class TestConvertUnicodeToHTML(unittest.TestCase):
  def test_success(self):
    unicode_str = "following Rowley\u2019s hand.\u201cOver the\u201d the 27-year-old"
    result = convert_unicode_to_html_entities(unicode_str)
    self.assertEqual(result, "following Rowley&#x2019;s hand.&#x201C;Over the&#x201D; the 27-year-old")

class TestGetArticleDate(unittest.TestCase):
  def test_get_article_text_guardian(self):
    with open('app/tests/sample_guardian_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      publish_date = get_article_date(soup, "https://www.guardian.co.tt/", None)
      self.assertEqual(publish_date, '2025-01-05')
  
  def test_get_article_text_express(self):
    with open('app/tests/sample_express_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      publish_date = get_article_date(soup, "https://trinidadexpress.com/", None)
      self.assertEqual(publish_date, '2025-01-05')
  
  def test_get_article_text_newsday(self):
    with open('app/tests/sample_newsday_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      publish_date = get_article_date(soup, "https://newsday.co.tt/category/news/", None)
      self.assertEqual(publish_date, '2025-01-05')

class TestGetArticleImg(unittest.TestCase):
  def test_get_article_img_guardian(self):
    with open('app/tests/sample_guardian_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      img_url = get_article_img(soup, "https://www.guardian.co.tt/", None)
      self.assertEqual(img_url, 'https://www.guardian.co.tt/image-3.5681143.620455.20250105012950.836a91ebcc')
  
  def test_get_article_img_express(self):
    with open('app/tests/sample_express_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      img_url = get_article_img(soup, "https://trinidadexpress.com/", None)
      self.assertEqual(img_url, 'https://bloximages.newyork1.vip.townnews.com/trinidadexpress.com/content/tncms/assets/v3/editorial/7/32/732bbf7a-cb88-11ef-b2cb-fb0aba2320a3/677abe38edb89.image.jpg?resize=400%2C267')
  
  def test_get_article_img_newsday(self):
    with open('app/tests/sample_newsday_article.html', 'r', encoding='utf-8') as article:
      html_content = article.read()
      soup = BeautifulSoup(html_content, 'html.parser')
      img_url = get_article_img(soup, "https://newsday.co.tt/category/news/", None)
      self.assertEqual(img_url, 'https://newsday.co.tt/wp-content/uploads/2024/11/police-file-photo.jpg')


if __name__ == "__main__":
    unittest.main()
