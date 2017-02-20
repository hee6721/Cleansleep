import sys
import os
from argparse import ArgumentParser
import csv
#import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
#from tokenization import my_sent_tokenizer, my_word_tokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import defaultdict
import cPickle as pickle
from nltk import sent_tokenize, word_tokenize
import re

#     print 
#     print 

    
#des = ""
def main():
    parser = ArgumentParser()
    parser.add_argument("--filename", type=str, dest="filename")
    args = parser.parse_args()
    print args

    openfile = args.filename
    print openfile

    index = openfile.find("_list_")
    hotel_tag = openfile[index+6:-4]
    print hotel_tag
    des = openfile[index+6:-4]+"/"    
    print des

#    path = "/Users/hkim/Desktop/Insight_Project/CleanSleep/"+des
    path = "/Users/hkim/Desktop/CleanSleep_Project/hotels_dic/"+des
    print path
    if not os.path.exists(path):
        os.makedirs(path)

    d={}

    with open(openfile, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for row in reader:
            #        print row[4]
            k = row[4]
            v = row[5]
            d[k] = v
#        print d

        raw_reviews = d
    # Convert raw text into sentences
        reviewids = raw_reviews.keys()
        sent_tokens_byreviewid = {}
        for reviewid in reviewids:
            rawtext = raw_reviews[reviewid]
            rawtext = rawtext.replace("/", " ")
            rawtext = str(unicode(rawtext, 'ascii', 'ignore'))
            rawtext = rawtext.lower()
            sent_tokens = sent_tokenize(rawtext)
#            print "sent_tokens"
#            print sent_tokens
            sent_tokens_fixed = []
            for sent in sent_tokens:
#                print sent
                while re.search("[a-zA-Z][!?.)][a-zA-Z]", sent):
                    x,y = re.search("[a-zA-Z][!?.)][a-zA-Z]", sent).span()
                    sent_tokens_fixed.append(sent[:x+2])
                    sent = sent[x+2:]
                    sent_tokens_fixed.append(sent)
                sent_tokens_byreviewid[reviewid] = sent_tokens_fixed
            sent_tokens_byreviewid[reviewid] = sent_tokens
#        print sent_tokens_byreviewid


    # Output data
#outfile = "%s/sent_tokens_byreviewid.pyvar" %args.folder
    outfile = path+hotel_tag+"_sent_tokens_byreviewid.pyvar"
#    outfile = "sent_tokens_byreviewid.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(sent_tokens_byreviewid, outfile)
    outfile.close()


    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer()
    lemma=True

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
#    print word_tokens_byreviewid

    outfile = path+hotel_tag+"_word_tokens_byreviewid.pyvar"
#    outfile = "word_tokens_byreviewid.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(word_tokens_byreviewid, outfile)
    outfile.close()


    # Label sentence words with parts of speech (POS-tagging)
    # Clean up the words (stemming)
    # Keep only nouns
    wnl = WordNetLemmatizer()
#    nouns = set(["NN", "NNS", "NNP", "NNPS"])
#     nouns = set(["NN", "NNS", "NNP", "NNPS","JJ","RB"])
    wordset = set(["JJ","JJR","JJS", "NN", "NNS", "NNP", "NNPS", "VB","VBD","VBG","VBN","VBP","VBZ"])
    pos_tags_byreviewid = {}
    for reviewid in reviewids:
        pos_tags_byreviewid[reviewid] = []
        for word_tokens in word_tokens_byreviewid[reviewid]:
            pos_tags = pos_tag(word_tokens)
            new_pos_tags = []
            for i in range(0, len(pos_tags)):
                w = pos_tags[i][0]
                p = pos_tags[i][1]
#                 if p in nouns:
                if p in wordset:
##                if p in selCate:
                    new_pos_tags.append((wnl.lemmatize(w), p))
            pos_tags_byreviewid[reviewid].append(new_pos_tags)
#    print  pos_tags_byreviewid                   
    # Output data
    outfile = path+hotel_tag+"_pos_tags_byreviewid.pyvar"
#    outfile = "pos_tags_byreviewid.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(pos_tags_byreviewid, outfile)
    outfile.close()

    # Find all the nouns
    all_wordset_tokens = []
    for reviewid in reviewids:
        sents = pos_tags_byreviewid[reviewid]
        for sent in sents:
            for word, pos in sent:
                if (word.isalpha()):
                    all_wordset_tokens.append(word)
                    
##Remove bad words
    ignore = set(stopwords.words('english'))
    all_wordset_tokens = set(all_wordset_tokens) - ignore

# Count document occurrence of each noun
    wordset_document_membership = defaultdict(int)
    for term in set(all_wordset_tokens):
        member_reviewids = []
        for reviewid in reviewids:
            for sent in pos_tags_byreviewid[reviewid]:
                for w, pos in sent:
                    if (w == term):
                        member_reviewids.append(reviewid)
        wordset_document_membership[term] = set(member_reviewids)
#    print noun_document_membership                        
    # Output data
    outfile = path+hotel_tag+"_wordset_document_membership.pyvar"
#    outfile = "noun_document_membership.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(wordset_document_membership, outfile)
    outfile.close()

if __name__ == "__main__":
    main()

# print "mkdir " + hotel_tag
# print "mv *.pyvar "+hotel_tag+"/"  

# path = "/Users/hkim/Desktop/Insight_Project/project/"+des

# if not os.path.exists(path):
#     os.makedirs(path)
# #os.mkdir(path,0777 );
# os.rename(r"[*]*.pyvar",des)
# #r_id = re.findall(r"-r([0-9]*)", url)
