##!/usr/bin/python 

import urllib2
import requests
from bs4 import BeautifulSoup
import re

base_url = "http://www.tripadvisor.com"

city_id = "g60763"
city =  "New_York_city"
state = "New_York"

# city_id = "g60713"
# city =  "San_Francisco"
# state = "California"

city_url = base_url + "/Tourism-"+city_id+"-"+city+"_"+state+"-Vacations.html"
print
print "city name is "+city+" and city's Id is " + city_id+"\n"
print city + "'s URL is "+city_url+"\n"


city_html = urllib2.urlopen(city_url) 
city_bsObj = BeautifulSoup(city_html)

for link in city_bsObj.findAll("a", {"data-trk":"hotels_nav"}): 
#    print link
    if 'href' in link.attrs:
        city_hotels_url = link.attrs['href']
        print base_url+city_hotels_url+"\n"
        print city +"'s Hotel list will be here : "+ base_url+city_hotels_url+"\n"

for child in city_bsObj.find("span", {"class":"typeName"}).children:
    types = child
#    print types

for child in city_bsObj.find("span", {"class":"typeQty"}).children:
    total_hotel_number = child[1:-1]
#   print type(total_hotel_number), total_hotel_number,"\n"
    total_hotel_number = float(total_hotel_number)
    
    if total_hotel_number/31 > int(total_hotel_number/31):
        hotel_pages= int(total_hotel_number/31) + 1 
    else:
        hotel_pages= int(total_hotel_number/31)

for child in city_bsObj.find("span", {"class":"contentCount"}).children:
    total_review_number = child[:child.find(" Reviews")]
#    print type(total_hotel_number), total_review_number,"\n"
    
#     if total__number/31 > int(total_hotel_number/31):
#         hotel_pages= int(total_hotel_number/31) + 1 
#     else:
#         hotel_pages= int(total_hotel_number/31)

print "Getting more hotels : "

list_page = [30]
count = 30
while count < total_hotel_number : 
    count +=30
    list_page.append(count)

print list_page

first_page = base_url+"/"+types+"-"+city_id+"-"+city+state+"-"+types+".html"
#print "1st page : "+"/"+types+"-"+city_id+"-"+city+state+"-"+types+".html"
print "1st page : " + first_page
hotel_page = [first_page]
for i in list_page[:-1] : 
    hotel_list_more = base_url+"/"+types+"-"+city_id+"-oa"+str(i)+"-"+city+state+"-"+types+".html#ACCOM_OVERVIEW"
    hotel_page.append(hotel_list_more)
    print hotel_list_more
print hotel_page

print city+"'s summary : \n"
print base_url+city_hotels_url+ "\n"
print "hotel type is "+ types + "\n"
print "total reviews are ",total_review_number,"\n"
print "total hotel in "+city+" is ",total_hotel_number,"\n"
print "therefore hotel pages are ", hotel_pages,"\n" 
print "------------next step--------------\n"
print "Go to "+base_url+city_hotels_url+" and find " + types +" list.\n"
print total_hotel_number," ",types+" will be on ",hotel_pages,"pages. Each pages has 31 "+types+".\n"

''' 
making hotel list url from all page. 
each page's url is in hotel_page
'''

hotel_url_list=[]
hotel_property_id_list = []
hotel_id_list=[]

#hotel_html = urllib2.urlopen(base_url+city_hotels_url) 
for url in hotel_page : 
    hotel_html = urllib2.urlopen(url)
    hotel_bsObj = BeautifulSoup(hotel_html)

#     print base_url+city_hotels_url
#     print

    city_hotels_review_url = ""
    for link in hotel_bsObj.findAll("a", {"class":"property_title"}):
        #     print link
        #     print
        if 'href' in link.attrs:
            city_hotels_review_url = link.attrs['href']
#            print city_hotels_review_url
            hotel_url_list.append(base_url+city_hotels_review_url)
#        print hotel_url_list
            
        if 'id' in link.attrs:
            hotel_property_id=link.attrs['id']
            hotel_property_id_list.append(hotel_property_id)
            index = hotel_property_id.find('property_')
            id = hotel_property_id[9:]
        #        print id
            hotel_id_list.append(id)

#        print hotel_id_list

# hotel_id_list=[]

# for link in hotel_bsObj.findAll("div", {"class":"listing easyClear  p13n_imperfect "}):
#     if 'data-locationid' in link.attrs:
#         hotel_id=link.attrs['data-locationid']
#         hotel_id_list.append(hotel_id)
# #        print hotel_id_list
''' dictionary '''
dict0 = dict(zip(hotel_id_list,hotel_property_id_list))
print dict0, len(dict0)
dict1 = dict(zip(hotel_id_list,hotel_url_list))
print dict1, len(dict1)

print        
#print hotel_url_list, len(hotel_url_list)
hotel_url_list = list(set(hotel_url_list))
print
print "removed doubled hotel_url_list \n"
print hotel_url_list, len(hotel_url_list)

print
#print hotel_property_id_list, len(hotel_property_id_list)
#hotel_property_id_list = list(set(hotel_property_id_list))
print
# print "removed doubled hotel_property_id_list \n"
# print hotel_property_id_list, len(hotel_property_id_list)

print
#print hotel_id_list, len(hotel_id_list)
#hotel_id_list = list(set(hotel_id_list))
print
# print "removed doubled one \n"
# print hotel_id_list, len(hotel_id_list)

file_hotel_list = "data/file_hotel_list-"+city+"-"+state+".html"

file = open(file_hotel_list, 'w')
for item in hotel_url_list:
    file.write("%s\n" % item)
file.close()

