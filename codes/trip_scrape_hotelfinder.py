##!/usr/bin/python 

import urllib2
import requests
from bs4 import BeautifulSoup
import re
import csv
import json
from argparse import ArgumentParser

'''
collect review form each hotel. 
all hotel url list  is hotel_url_list

'''

base_url = "http://www.tripadvisor.com"
city_id = "g60763"
city =  "New_York_city"
state = "New_York"

hotel_info_list = []   
hotel_name_list = []

def main():

    parser = ArgumentParser()
#    parser.add_argument("--folder", type=str, dest="folder")
    parser.add_argument("--link", type=str, dest="link")
    args = parser.parse_args()

    url =  args.link
    print url , type(url)
    h = re.findall(r"-Reviews-([a-zA-Z0-9\_]*)", url) 
    hotelname = h[0]
#    hotelname = args.folder
    print hotelname+" review page collecting start"
    print

# #    http://www.tripadvisor.com/Hotel_Review-g60763-d256738-Reviews-Envoy_Club_Suites-New_York_City_New_York.html
#     open_file = "data/file_hotel_list-"+city+"-"+state+".html"
#     hotel_list_file = open(open_file,'r') 
#     print open_file
#     for line in hotel_list_file:

#         if line.find(hotelname):
#             print line


    url = args.link 
    print url
    review_html = urllib2.urlopen(url)
    review_bsObj = BeautifulSoup(review_html.read()) 

    data_locid = re.findall(r"-d([0-9\_]*)", url) 
    print data_locid[0]
    
    for link in review_bsObj.findAll("a",{"class":"more taLnk"}):
#        print link 
        if 'content' in link.attrs:
            total_review = int(link.attrs['content'])
#            print total_review, type(total_review)
            total_review_page = total_review/10+1
                  
        review_url_list=[]
    
        for link in review_bsObj.findAll("div",{"class":"reviewSelector"}):
            if 'id' in link.attrs:
                #            print link.attrs['id']
                input_id = link.attrs['id']
                input_id_new = input_id.replace('review_','rn')
                input_id_url = input_id.replace('review_','r')
                hotel_name_url= hotelname
         #       print hotel_name_url
                review_ind_url = "/ShowUserReviews-"+city_id+"-d"+data_locid[0]+"-"+input_id_url+"-"+hotel_name_url+"-"+city+"_"+state+".html#CHECK_RATES_CONT"
            #            print review_ind_url
                review_url_list.append(base_url+review_ind_url)

#                print review_ind_url

        print "Getting more hotels reviews : "
        list_page = [10]
        count = 10
        while count < total_review : 
            count +=10
            list_page.append(count)
#            print list_page
            
        first_page = url
#        print "1st review page : "+ first_page
        review_page= [first_page[:-1]]
        for i in list_page[:-1] :
            index = first_page.find("-Reviews-")
            review_list_more = first_page[:index]+"-or"+str(i)+first_page[index:-1] 
#            print review_list_more
            review_page.append(review_list_more)
#    print review_page, len(review_page)

        for line in review_page[1:]:
            #    print line
            url = line 
        #    print url
            review_html = urllib2.urlopen(url)
            review_bsObj = BeautifulSoup(review_html.read()) 
            
            for link in review_bsObj.findAll("div",{"class":"reviewSelector"}):
                if 'id' in link.attrs:
                    #            print link.attrs['id']
                    input_id = link.attrs['id']
                    input_id_new = input_id.replace('review_','rn')
                    input_id_url = input_id.replace('review_','r')
                    hotel_name_url= hotelname
#                    print hotel_name_url

                    review_ind_url = "/ShowUserReviews-"+city_id+"-d"+data_locid[0]+"-"+input_id_url+"-"+hotel_name_url+"-"+city+"_"+state+".html#CHECK_RATES_CONT"
                #            print review_ind_url
                    review_url_list.append(base_url+review_ind_url)
                
        hotel_name_list.append(hotel_name_url)
#        print review_url_list, len(review_url_list)
    

    file_hotel_review = "data/file_hotel_review_list-"+hotel_name_url+"-"+city+"-"+state+".html"
    file = open(file_hotel_review, 'w')
    for item in review_url_list:
        file.write("%s\n" % item)
    file.close()


if __name__ == "__main__":
    main()
