##!/usr/bin/python 

import urllib2
import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import codecs
import sys

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

'''
collect hotel infomation. 
all hotel url list  is hotel_url_list

'''

base_url = "http://www.tripadvisor.com"
city_id = "g60763"
city =  "New_York_city"
state = "New_York"

open_file = "data/file_hotel_list-"+city+"-"+state+".html"
#open_file = "data/file_hotel_review-Hampton_Inn_Madison_Square_Garden-New_York_city-New_York.html"
print open_file
#hotel_list_file = open("dummy.tex",'r') 
hotel_list_file = open(open_file,'r') 

hotel_info_list = []   
hotel_name_list = []
for line in hotel_list_file:
    print
    print
    print line
    url = line 
    review_html = urllib2.urlopen(url)
    review_bsObj = BeautifulSoup(review_html.read()) 

#     hotelName0=review_bsObj.h1.string
#     print
#     print"-------"+ hotelName0+" start---------"
#     hotel_name_list.append(hotelName0)

    review_url_list=[]

    for link in review_bsObj.findAll("a",{"class":"more taLnk"}):
#       print link 
        if 'content' in link.attrs:
            total_review = int(link.attrs['content'])
#            print total_review, type(total_review)
            total_review_page = total_review/10+1
            
        
    for child in review_bsObj.find("span",{"class":"street-address"}).children:
        addre0= child
#        print child
    for child in review_bsObj.find("span",{"property":"addressLocality"}).children:
        addre1= child
#        print child
    for child in review_bsObj.find("span",{"property":"addressRegion"}).children:
        addre2= child
#        print child


    for link in review_bsObj.findAll("div",{"class":"mapContainer"}):
#        print link
        if 'data-lat' in link.attrs:
            data_lat = link.attrs['data-lat']
#            print data_lat
        if 'data-lng' in link.attrs:
            data_lng = link.attrs['data-lng']
#            print data_lng
        if 'data-name' in link.attrs:
            data_name = link.attrs['data-name']
            print data_name, type(data_name)
        if 'data-locid' in link.attrs:
            data_locid = link.attrs['data-locid']
#            data_locid = int(data_locid)
#            print data_locid
        print

    for link in review_bsObj.findAll("div",{"class":"reviewSelector"}):
        if 'id' in link.attrs:
#            print link.attrs['id']
            input_id = link.attrs['id']
            input_id_new = input_id.replace('review_','rn')
            input_id_url = input_id.replace('review_','r')
#             print input_id_new, input_id_url
#             print
#             print data_name
            hotel_name_url0= data_name.replace(" ","_")
#            print hotel_name_url0
            hotel_name_url1= hotel_name_url0.replace("_-_","_")
            hotel_name_url2= hotel_name_url1.replace(",","_")
            hotel_name_url3= hotel_name_url2.replace("/","_")
            hotel_name_url4= hotel_name_url3.replace("-","_")
            hotel_name_url= hotel_name_url4
#             removeSpecialChars = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", " ", hotel_name_url0)
#             hotel_name_url = hotel_name_url0
#            print hotel_name_url, type(hotel_name_url)
#            review_ind_url = "/ShowUserReviews-"+city_id+"-d"+data_locid+"-"+input_id_url+"-"+hotel_name_url+"-"+city+"_"+state+".html#CHECK_RATES_CONT"
            review_ind_url = "/ShowUserReviews-"+city_id+"-d"+data_locid+"-"+input_id_url+"-"+hotel_name_url+"-"+city+"_"+state+".html#CHECK_RATES_CONT"
#            print review_ind_url
            review_url_list.append(base_url+review_ind_url)

#     print "-------------"+data_name+" Hotel summary---------------"    
#     print "Hotel id = ",data_locid
#     print "\nHotel Name : " + hotel_name_url
#     print "\nAddress :  "+addre0+","+addre1+","+addre2+"\n"
#     print "GPS Location : (",data_lat,",",data_lng,")"
#     print "\nTotal reviews of this property : ",total_review
#     print "\nTherefore, the total review pages are  ", total_review_page
#     print
#     print "\n-------------"+data_name+" Hotel summary End ---------------\n"    

    #            review_ind_url=review_ind_url.encode('utf-8')
    #            print "after encode : "+review_ind_url

#     data_name.decode('utf-8')
#     print "after decpde :"+data_name
#     data_name.find("-").replace("\u2013"," ")    
#     print "data_name  :  " + data_name
#     import unicodedata
#     if type(hotel_name_url) is unicode :
        
#        unicodedata.normalize('NFKD', hotel_name_url).encode('ascii','ignore')
        
    hotel_info = []

    hotel_info = [data_locid,str(hotel_name_url),addre0,addre1,addre2,data_lat,data_lng,total_review,total_review_page]
    hotel_info_list.append(hotel_info)
#    print hotel_info
#    print hotel_info_list
#     print
#     print len(hotel_info_list)

    hotel_name_list.append(hotel_name_url)

heading = ['ID','HotelName','Address','City','State','data-lat','data-len','TotalReview','TotalReviewPages']
print " hotel_info saving in csv file .. "
with open('data/hotel_info.csv', 'wb') as f:
    writer = csv.writer(f, delimiter = ';')
    writer.writerow(heading)
    for row in hotel_info_list:
        writer.writerow(row)
f.close()

# print "hotel name file is saving"
# print hotel_name_list
# f0 = open('data/hotel_name.txt','wb')
# for item in hotel_name_list : 
#     f0.write("%s\n"%item)
# f0.close()
# # json.dump(hotel_name_list,f0)
