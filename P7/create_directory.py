import os
def create_directory(scrapping):
    if not os.path.exists(scrapping):
        os.makedirs(scrapping)
        
create_directory('scrapping')