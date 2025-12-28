import requests
from bs4 import BeautifulSoup
import pandas as pd

#menambakan url
url ="https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"

pages = requests.get(url)