from argparse import ArgumentParser
from collections import defaultdict
import cPickle as pickle
import sys 
import os
import pandas as pd 
import csv
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import re

def my_sent_tokenizer(raw_reviews):
    # Convert raw text into sentences
    reviewids = raw_reviews.keys()
    sent_tokens_byreviewid = {}
    for reviewid in reviewids:
        rawtext = raw_reviews[reviewid]
        rawtext = rawtext.replace("/", " ")
        rawtext = str(unicode(rawtext, 'ascii', 'ignore'))
        rawtext = rawtext.lower()
        sent_tokens = sent_tokenize(rawtext)
        sent_tokens_fixed = []
        for sent in sent_tokens:
            while re.search("[a-zA-Z][!?.)][a-zA-Z]", sent):
                x,y = re.search("[a-zA-Z][!?.)][a-zA-Z]", sent).span()
                sent_tokens_fixed.append(sent[:x+2])
                sent = sent[x+2:]
            sent_tokens_fixed.append(sent)
        sent_tokens_byreviewid[reviewid] = sent_tokens_fixed
    return sent_tokens_byreviewid

wnl = WordNetLemmatizer()
def my_word_tokenizer(sent_tokens_byreviewid, lemma=False):
    # Convert setences into words
    reviewids = sent_tokens_byreviewid.keys()
    word_tokens_byreviewid = {}
    for reviewid in reviewids:
        sent_tokens = sent_tokens_byreviewid[reviewid]
        word_tokens_byreviewid[reviewid] = []
        for sent in sent_tokens:
            word_tokens = word_tokenize(sent)
	    if lemma:
		word_tokens = [wnl.lemmatize(word) for word in word_tokens]
            word_tokens_byreviewid[reviewid].append(word_tokens)
    return word_tokens_byreviewid


def main():
    parser = ArgumentParser()
#    parser.add_argument("--folder", type=str, dest="folder")
    parser.add_argument("--filename", type=str, dest="filename") ## data/merge_reviews.csv
    args = parser.parse_args()
    print args

    openfile = args.filename
    print openfile

    d = {}
    dr = {}

    with open(openfile, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for row in reader:
            k = row[4]
            v = row[5]
            vr = row[6]
            d[k] = v
            dr[k] = vr

##    outfile = args.folder+"/"+args.folder+"_reviewtext.pyvar"
    outfile = "NB_data/NB_reviewtext.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(d, outfile)
    outfile.close()

    keepreviewids = defaultdict(list)
    raw_reviews = {}

#    infile = args.folder+"/"+args.folder+"_reviewtext.pyvar"
    infile = "NB_data/NB_reviewtext.pyvar"
    infile = open(infile, 'r')
    ratings_byreviewid = pickle.load(infile)
    raw_reviews.update(ratings_byreviewid)
    infile.close()

  
    # Keep extreme reviews                                                                                         
    reviewids = dr.keys()
    numkept = 0
    print len(reviewids)
    # Keep extreme reviews

    for reviewid in reviewids:
#        print dr[reviewid] , type(dr[reviewid]), type(int(dr[reviewid])) 
        #stars = ratings_byreviewid[reviewid]
        stars = dr[reviewid]
#        stars = int(s)
#        print type(stars)
#        stars = int(dr[reviewid])
#        print stars
        if stars in ['1', '5']:
            keepreviewids[stars].append(reviewid)
            numkept += 1
        else:
            del raw_reviews[reviewid]
#        print keepreviewids
    #    print raw_reviews.key()
    print "%5d extreme reviews " %numkept
    
    print "%5d 1-star reviews" %len(keepreviewids['1'])
    print "%5d 5-star reviews" %len(keepreviewids['5'])
    reviewids = keepreviewids['1'] + keepreviewids['5']


    sent_tokens_byreviewid = my_sent_tokenizer(raw_reviews)

    word_tokens_byreviewid = my_word_tokenizer(sent_tokens_byreviewid, lemma=True)

    # Output the tokenized reviews
    outfile = "NB_data/NB_trainingdata.wordtokens.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(sent_tokens_byreviewid, outfile)
    outfile.close()

    outfile = "NB_data/NB_trainingdata.senttokens.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(word_tokens_byreviewid, outfile)
    outfile.close()

    # Output the training reviewids
    outfile = "NB_data/NB_trainingdata.labels.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(keepreviewids, outfile)
    outfile.close()


if __name__ == "__main__":
    main()
