#!/urs/bin/python

import pandas as pd 
import glob

interesting_files = glob.glob("data/hotel_review_rate_list_*.csv") 

header_saved = False
with open('data/merge_reviews.csv','wb') as fout:
    for filename in interesting_files:
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                fout.write(header)
                header_saved = True
            for line in fin:
                fout.write(line)

