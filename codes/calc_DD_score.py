from argparse import ArgumentParser
from nltk import WordNetLemmatizer
#from sent_features import get_sent_features
from feature_extrac import get_sent_features
from math import pow
import cPickle as pickle
import sys, os
import re
import csv
import datetime
from dateutil.relativedelta import * 
from datescore import *

def delete_terms(term_dict, bad_terms):
    all_terms = term_dict.keys()
    for term in all_terms:
	if term in set(bad_terms):
	    del term_dict[term]
    return


# Get the sentence ids with the term of interest
def get_sentence_ids(sentences, term):
    sentence_ids = []
    n_sent = len(sentences)
    for sent_id in range(0, n_sent):
        for word, postag in sentences[sent_id]:
            if word == term:
		sentence_ids.append(sent_id)
                break
    return sentence_ids

# Determine if a term is rare or common or inbetween
# If common, determine if average, above avg, below avg
def compare_to_average(uniques, commons, term, sentiment):
    if term in commons:
        avg, stdev = commons[term]
        if sentiment > avg + stdev:
            return "class_icons-03.png"   # above average
        elif sentiment < avg - stdev:
            return "class_icons-01.png"  # below average
        else:
            return "class_icons-02.png"  # average
    elif term in uniques: 
            return "class_icons-04.png" # unique
    else:
	    return  # not common or unique


def main():
    parser = ArgumentParser()
    parser.add_argument("--filename", type=str, dest="filename")
#     parser.add_argument("--folder", type=str, dest="folder")
#     parser.add_argument("--cutoff", type=float, dest="cutoff")
    args = parser.parse_args()
    print args
#     hotelname = args.folder.split("/")[1]
    openfile = args.filename

    index = openfile.find("_list_")
    hotel_tag = args.filename[index+6:-4]
#     hotelname = hotel_tag.replace("_"," ")
    hotelname = hotel_tag
#     idx = openfile.find("_list_")
#     hotelID = hotelname[:]
    print hotel_tag, hotelname
    des = openfile[index+6:-4]+"/"    
    print des

    path = "/Users/hkim/Desktop/CleanSleep_Project/hotels_dic/"+des
    print path
    if not os.path.exists(path):
        os.makedirs(path)


    # Load the NB classifier
    infile = "NB_data/NB_sentiment.model.pyvar"
    infile = open(infile, 'r')
    classifier = pickle.load(infile)
    infile.close()

    dates = {}
    filename = openfile
    print filename
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for row in reader:
            #        print row[4]
            k = row[4]
            v = row[2]
            dates[k] = v
#    print dates
 #   filename.close()
    num_reviews = len(dates.keys())
    print num_reviews

    # Load the term - reviewid mapping
#     filename = "%s/%s_wordset_document_membership.pyvar" %(hotel_tag,hotel_tag)
    filename = "%s/%s_wordset_document_membership.pyvar" %(path,hotel_tag)
    filename = open(filename, 'r')
    wordset_reviewids = pickle.load(filename)
    filename.close()

#     bad_terms = []

#     # Remove infrequent terms and single letters
#     for term in wordset_reviewids:
#         count = len(wordset_reviewids[term])
# #        print count, num_reviews*args.cutoff
#         if count < num_reviews*args.cutoff:
#             bad_terms.append(term)
#         elif len(term) == 1:
#             bad_terms.append(term)

#     # Remove bad terms
#     delete_terms(wordset_reviewids, bad_terms)

    # Load POS tagged words
    filename = "%s/%s_pos_tags_byreviewid.pyvar" %(path,hotel_tag)
    filename = open(filename, 'r')
    pos_tags_byreviewid = pickle.load(filename)
#    print filename
    filename.close()

    # Load the sentences
    filename = "%s/%s_sent_tokens_byreviewid.pyvar" %(path,hotel_tag)
    filename = open(filename, 'r')
    sent_tokens_byreviewid = pickle.load(filename)
#    print filename
    filename.close()

    # Load the sentences with words split out
    filename = "%s/%s_word_tokens_byreviewid.pyvar" %(path,hotel_tag)
    filename = open(filename, 'r')
    word_tokens_byreviewid = pickle.load(filename)
#    print filename
    filename.close()

#     # Load the term averages and standard deviations
#     filename = "term_averages.pyvar"
#     filename = open(filename, 'r')
#     uniques, middle, commons = pickle.load(filename)
#     filename.close()

    wnl = WordNetLemmatizer()

    # Define the list of frequent terms
    freqterms = wordset_reviewids.keys()

#     outfile1 = "%s/%s_hotelterms.tab" %(hotel_tag,hotel_tag)
    outfile1 = "%s/%s_hotelterms.tab" %(path,hotel_tag)
    print outfile1
    outfile1 = open(outfile1, 'w')
#     outfile2 = "%s/%s_mapping.tab" %(hotel_tag,hotel_tag)
    outfile2 = "%s/%s_mapping.tab" %(path,hotel_tag)
    print outfile2
    outfile2 = open(outfile2, 'w')

    for term_id in range(0, len(freqterms)):
	freqterm = freqterms[term_id]
        reviewids_forterm = wordset_reviewids[freqterm]

        # Determine a score for the review dates
# 	review_dates = [int(dates[reviewid]) for reviewid in reviewids_forterm]
 	review_dates = [dates[reviewid] for reviewid in reviewids_forterm]
#         print review_dates, type(review_dates)

        dscore = get_date_score(review_dates)
#         print "dscore is ",dscore

        sents_as_words = []
        for reviewid in reviewids_forterm:
	    sent_ids = get_sentence_ids(pos_tags_byreviewid[reviewid], freqterm)
	    for sent_id in sent_ids:
                outfile2.write("%s\t%s\t%s\t%s\n" %(hotelname, term_id, reviewid, sent_id))
		sents_as_words.append(word_tokens_byreviewid[reviewid][sent_id])

        predictions = []
        for i in range(0, len(sents_as_words)):
	    words = [wnl.lemmatize(word) for word in sents_as_words[i]]
	    words = [word for word in words if word != freqterm]
            pred = classifier.classify(get_sent_features(words))
	    predictions.append(pred)
        pos_percent = round(100.0*predictions.count("pos")/len(predictions),2)
        neg_percent = round(100.0*predictions.count("neg")/len(predictions),2)

# 	# Determine how this sentiment compares to other hotels
# 	label = compare_to_average(uniques, commons, freqterm, pos_percent)

#         num_term = len(noun_reviewids[freqterm])
#         outfile1.write("%s\t%s\t%s\t%s\t%.3f\t%s\t%.2f\t%s\n" %(hotelname, term_id, 
#                       freqterm, num_term, 100.0*num_term/num_reviews, pos_percent, dscore, label))

        num_term = len(wordset_reviewids[freqterm])
        outfile1.write("%s\t%s\t%s\t%s\t%.3f\t%s\t%s\t%.3f\n" %(hotelname, term_id, 
                      freqterm, num_term, 100.0*num_term/num_reviews, pos_percent,neg_percent, dscore))

    outfile1.close()
    outfile2.close()


if __name__ == "__main__":
    main()
