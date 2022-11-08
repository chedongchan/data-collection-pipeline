import requests
from bs4 import BeautifulSoup 
import re
import json


url = 'https://www.imdb.com/title/tt0110912/fullcredits/?ref_=tt_cl_sm.html'
response = requests.get(url)
info = response.content
soup = BeautifulSoup(info, 'html.parser')
sections = soup.find(class_="cast_list")
cast_data = sections.find_all('tr')[1:]
cast_list=[]
cast_individual_links =[]

for person in cast_data:
    info = person.find_all('a')
    image_tag = person.find('img')
    info = [feature.text for feature in info]
    
    if len(info) == 3 and image_tag != 'NoneType':
        individual_link= person.a.attrs
        images, name, role = info
        dict = {
            "name":name,
            "role":role,
           
        }

        cast_individual_links.append(individual_link)
        actor_link = individual_link['href']
        actor_url = "https://www.imdb.com"+ str(actor_link)
        actor_response = requests.get(actor_url)
        movies = actor_response.content
        moviesoup = BeautifulSoup(movies, 'html.parser')
        filmography = moviesoup.find_all("div",class_="filmo-category-section")
        # print(len(filmography))
        # print(filmography[0].prettify())
        film_list = []
        year_list = []
        film_year_dict = {}
        for film in filmography[0]:
            film_name = film.find('a')
            film_year = film.find('span')
            if film_name != -1 and film_year != -1:
                if len(film_name) > 0 and len(film_year) > 0:
                    film_list.append(film_name.string)
                    film_year_num = re.findall(r'\d+',film_year.string)
                    film_year_single = ''.join(film_year_num)
                    year_list.append(film_year_single)
                    film_year_dict.update({film_name.string: film_year_single})
        dict.update( {"movies": film_year_dict })

    elif len(info) ==2 and image_tag == 'NoneType':
        images,name, role = info
        dict = {
            "name":name,
            "role":role,
            "movie":''
        }
    with open('cast_data_from_imdb.txt','a') as f:
        f.write(json.dumps(dict))
        f.write('\n')

    cast_list.append(dict) 

# read_file = pd.read_csv(r"C:\Users\dongc\Desktop\Code\python\AiCore\data-collection-pipeline\cast_data_from_imdb.txt")
# read_file.to_csv(r"C:\Users\dongc\Desktop\Code\python\AiCore\data-collection-pipeline\cast_data_from_imdb.csv", index=None)

# print(cast_list)   
# print(cast_individual_links)


# for i in range (len(cast_individual_links)):
#     actor_link = cast_individual_links[i]['href']
#     actor_url = "https://www.imdb.com"+ str(actor_link)
#     actor_response = requests.get(actor_url)
#     movies = actor_response.content
#     moviesoup = BeautifulSoup(movies, 'html.parser')
#     filmography = moviesoup.find_all("div",class_="filmo-category-section")
#     # print(len(filmography))
#     # print(filmography[0].prettify())
#     film_list = []
#     year_list = []
#     film_year_dict = {}
#     for film in filmography[0]:
#         film_name = film.find('a')
#         film_year = film.find('span')
#         if film_name != -1 and film_year != -1:
#             if len(film_name) > 0 and len(film_year) > 0:
#                 film_list.append(film_name.string)
#                 film_year_num = re.findall(r'\d+',film_year.string)
#                 film_year_single = ''.join(film_year_num)
#                 year_list.append(film_year_single)
#                 film_year_dict.update({film_name.string: film_year_single})

#     print(film_year_dict)

