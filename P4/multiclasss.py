from bs4 import BeautifulSoup
soup = BeautifulSoup('<html><body><div class="class1">''</div><div class="class2"></div><div class="class3"></div></body></html>')
soup.findAll, {"class1", "class2", "class3"}
