import requests
from bs4 import BeautifulSoup 

def get_property_data(url,address,type,price):
    response = requests.get(url)
    info = response.content
    soup = BeautifulSoup(info, 'html.parser')
    property_list_heading = soup.find('div', attrs={'data-testid': 'regular-listings'})
    next_page_link_title = soup.find('div', attrs={'data-testid': 'pagination'})
    for property in property_list_heading:
        address.append(property.h3.string)
        price.append(property.p.string)
        type.append(property.h2.string)

    property_data = {
        'Address':address,
        'Property Type':type,
        'Price':price,
    }

    return next_page_link_title, property_data

def next_page_collect(next_page_link_title):   

        next_page_atags = next_page_link_title.find_all('a')
        href=next_page_atags[-1]['href']
        next_page_url = str('https://www.zoopla.co.uk' + href)
       
        return next_page_url

address = []
type = []
price = []
url = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"

for i in range(5): 
    current_page, property_data = get_property_data(url,address,type,price)
    url = next_page_collect(current_page)
    i +=1

print(property_data)
print(len(property_data['Address']))
print(len(property_data['Property Type']))
print(len(property_data['Price']))



    
        
    
    




