from bs4 import BeautifulSoup
import requests
from degreescraper import get_courses

print(get_courses("Computer Science", "BS", "Intelligence & Information Internetworks"))