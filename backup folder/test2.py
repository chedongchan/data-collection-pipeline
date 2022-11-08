import json
import requests
from PIL import Image
import shutil
import urllib
file_dir = 'C:\\Users\\dongc\\Desktop\\Code\\python\\AiCore\\data-collection-pipeline\\raw_data\\Djams-1\\Djams-1 soundcloud info.json'
save_dir= 'C:\\Users\\dongc\\Desktop\\Code\\python\\AiCore\\data-collection-pipeline\\raw_data\\Djams-1\\'
with open(file_dir, 'r') as handle:
    parsed= json.load(handle)
    print(type(parsed))
    djams_1_img_links=parsed['Details']['Image Link']
    image_links= []
    i=0
    for link in djams_1_img_links:
        
        print(type(link))
        print(link)
        image_links.append(link)
        url= link.replace('"', "")
        url_new = url.replace("https","http")
        response= requests.get(url_new)
        if response.status_code:
            fp=open(f'{save_dir}\\{i}.jpg','wb')
            fp.write(response.content)
            fp.close()
        i+=1

