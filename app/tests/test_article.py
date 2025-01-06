import unittest
import sys
import os
import logging

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the directory above
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

logging.disable()

from article import Article

class TestArticle(unittest.TestCase):
  def test_get_article_data(self):
    article = Article("https://example.com", "Something happened somewhere", "https://example.com/something")
    result = {'base_url': 'https://example.com', 'headline': 'Something happened somewhere', 'url': 'https://example.com/something', 'img_url': None, 'article_body': None}
    self.assertEqual(article.get_article(), result)
    