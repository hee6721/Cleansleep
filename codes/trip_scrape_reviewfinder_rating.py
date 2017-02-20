#!/usr/bin/python 

import urllib2
import requests
#import urlopen
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import datetime
import time
import sys
import glob
from subprocess import Popen, PIPE
from argparse import ArgumentParser

base_url = "http://www.tripadvisor.com"
city_id = "g60763"
city =  "New_York_city"
state = "New_York"

hotel_review_rate_list = []

def main():

    parser = ArgumentParser()
    parser.add_argument("--folder", type=str, dest="folder")
    args = parser.parse_args()
    hotelname = args.folder

    print hotelname+" review start"
    print
    open_file = "data/file_hotel_review-"+hotelname+"-"+city+"-"+state+".html"
    print open_file
    input_file = open(open_file,'r')
    
    
    for line in input_file:
        #    print line
        url = line 
#        time.sleep(1)
        review_html = urllib2.urlopen(url)
        review_bsObj = BeautifulSoup(review_html.read()) 
    #print url
    #        print
        
        for link in review_bsObj.findAll("span",{"class":"ratingDate"}):
            if 'content' in link.attrs:
                review_date =  link.attrs['content']
#                print review_date, type(review_date)
                
                Date = datetime.datetime.strptime(review_date, "%Y-%m-%d")
#                print Date, type(Date)

                index_time = datetime.datetime(2006,1,1)  
                if  Date > index_time :
                
                    hotel_id = re.findall(r"-d([0-9]*)", url)
#                    print hotel_id[0], type(hotel_id[0])
                    
                    r_id = re.findall(r"-r([0-9]*)", url)
#                    print r_id[0]
                    
                    review_id = "review_"+r_id[0]
#                    print review_id

                    Crating = 0
                    for link in review_bsObj.findAll("div",{"id":review_id},{"class":"v"}):
            #            for link in review_bsObj.findAll("div", {"class":"rating-list"}):
            #            print link
                        for link1 in link.findAll("li",{"class":"recommend-answer"}):
                #                 print link1
                #                print link1.text , type(link1.text)
                            l0 = str(link1)
                #                print l0 , type(l0)
                            if "Cleanliness" in l0:
                    #                    print "l0 is "+ l0

                                hotel_id = re.findall(r"-d([0-9]*)", url)
                    
                                index_s = "<img alt=\""
                                r0 = re.findall(r"<img alt=\"[0-9*]", l0) 
#                                print r0[0][10:]
                                Crating = int(r0[0][10:])

                
                        for link in review_bsObj.findAll("p",{"id":review_id},):
            #        for link in review_bsObj.findAll("div",{"class":"col2of2"},):
            #            print link
                            r0 =str(link)
            #            print r0 , type(r0)
                            r1 = re.compile(r'<.*?>')
                            review = r1.sub('',r0)
            #            r1=r0.replace("^<[A-za-z0-9*\"\=\\]$>","")
#                            print review

                            hotel_review_rate = []
                            hotel_review_rate = [hotel_id[0],hotelname,Date,review_id,r_id[0],review,Crating]
                            hotel_review_rate_list.append(hotel_review_rate)

#    print hotel_review_rate_list

    heading = ['ID','HotelName','ReviewDate','ReviewId','ReviewId_number','Review','Cleanliness']
    print " hotel_review_rate_list saving in csv file .. "
    outfile = "data/hotel_review_rate_list_"+hotel_id[0]+"_"+hotelname+".csv"
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(heading)
        for row in hotel_review_rate_list:
            writer.writerow(row)
    f.close()

if __name__ == "__main__":
    main()
