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

from articlelist import ArticleList
from article import Article

# to implement
class TestArticleList(unittest.TestCase):
  pass
