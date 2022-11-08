import requests
from bs4 import BeautifulSoup 

url = 'https://www.imdb.com/title/tt0110912/fullcredits/?ref_=tt_cl_sm.html'
response = requests.get(url)
info = response.content
soup = BeautifulSoup(info, 'html.parser')
sections = soup.find_all('img')
print(sections)
cast_data = sections.find_all('tr')[1:]
cast_list = []
for person in cast_data:
    info = person.find_all('a')
    image_tag = person.find('img')
    # for tag in info[0]:
    #     print(tag['src'])
    info = [feature.text for feature in info]
    if len(info) == 3 and image_tag != 'NoneType':
        images,name, role = info
        dict = {
            "name":name,
            "role":role,
            "image_link":''    
    
        }
    
    elif len(info) ==2 and image_tag == 'NoneType':
        images,name, role = info
        dict = {
            "name":name,
            "role":role,
            "image_link":''
        }
    cast_list.append(dict)

# print (cast_list)    # image, name, role = info
    
# print (image, name, role)


    
