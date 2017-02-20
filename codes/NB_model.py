from argparse import ArgumentParser
from nltk.classify import NaiveBayesClassifier
from nltk import FreqDist
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from feature_extrac import get_sent_features, get_bad_words
from collections import defaultdict
from pandas import DataFrame
import nltk.classify.util
import cPickle as pickle
import random
from nltk.draw.dispersion import dispersion_plot
from sklearn import cross_validation

def make_folds(vector, n):
    return [vector[i:i+n] for i in range(0, len(vector), n)]


def eval_classifier(traindata, testdata):
    classifier = NaiveBayesClassifier.train(traindata)
    truthsets = defaultdict(set)
    testsets = defaultdict(set)
 
    for i, (features, label) in enumerate(testdata):
        truthsets[label].add(i)
        prediction = classifier.classify(features)
        testsets[prediction].add(i)

    accuracy = nltk.classify.util.accuracy(classifier, testdata)
    posprecision = nltk.metrics.precision(truthsets['pos'], testsets['pos'])
    posrecall = nltk.metrics.recall(truthsets['pos'], testsets['pos'])
    negprecision = nltk.metrics.precision(truthsets['neg'], testsets['neg'])
    negrecall = nltk.metrics.recall(truthsets['neg'], testsets['neg'])
    return accuracy, posprecision, posrecall, negprecision, negrecall


def main():
#     parser = ArgumentParser()
#     parser.add_argument("--folder", type=str, dest="folder")
#     args = parser.parse_args()
#     hotelname = args.folder

    # Load the tokenized reviews (sentences)
#    infile = args.folder+"/"+hotelname+"_NB_trainingdata.senttokens_sel.pyvar"
    infile = "NB_data/NB_trainingdata.senttokens.pyvar"
    infile = open(infile, 'r')
    print infile
    word_tokens_byreviewid = pickle.load(infile)
    infile.close()

    # Load the training reviewids
#    infile = args.folder+"/"+hotelname+"_NB_trainingdata.labels.pyvar"
    infile = "NB_data/NB_trainingdata.labels.pyvar"
    infile = open(infile, 'r')
    keepreviewids = pickle.load(infile)
    infile.close()

    word_tokens_byreviewid_expanded = {}
    negtags = []; postags = []
    for reviewid in word_tokens_byreviewid:
        sents = word_tokens_byreviewid[reviewid]
        for sent_idx in range(0, len(sents)):
            tag = (reviewid, str(sent_idx))
            word_tokens_byreviewid_expanded[tag] = sents[sent_idx]
            if reviewid in keepreviewids['1']:
                negtags.append(tag)
            if reviewid in keepreviewids['5']:
                postags.append(tag)
    print "neg sents: %d\t pos sents: %d" %(len(negtags), len(postags))

#     # Stem the words in the sentences
#     # Separate each sentence into a unique entry
#     word_tokens_byreviewid_expanded = {}
#     negtags = []; postags = []
#     tag_expanded = []
#     for reviewid in word_tokens_byreviewid:
#         sents = word_tokens_byreviewid[reviewid]
# 	for sent_idx in range(0, len(sents)):
# 	    tag = (reviewid, str(sent_idx))
#             tag_expanded.append(tag)
# #             print tag
# # 	    print sents[sent_idx]
#             word_tokens_byreviewid_expanded[tag] = sents[sent_idx]
            
# 	    if reviewid in keepreviewids[0]:
#                 negtags.append(tag)
# #                 print "negtag : "
# #                 print tag
# #                 print negtags
# 	    if reviewid in keepreviewids[1]:
# 		postags.append(tag)
#     print "neg sents: %d\t pos sents: %d" %(len(negtags), len(postags))

#     print negtags, len(negtags), len(set(negtags))
#     print
# #    print postags
#    print word_tokens_byreviewid_expanded
#     print tag_expanded
#     print word_tokens_byreviewid_expanded[tag_expanded]

#     all_words = []
#     # Get all words to analyze frequency of unigrams and bigrams
#     for t in tag_expanded : 
#         print tag
#         tag = t 
#         word = word_tokens_byreviewid_expanded[tag]

#         token=nltk.word_tokenize(word)
# #        print len(token)
    
#         for i  in range (0, len(token)): 
#             all_words.append(token[i])
# #    all_words = [word for tag in word_tokens_byreviewid_expanded for word in word_tokens_byreviewid_expanded[tag]]
# #    all_words =word_tokens_byreviewid_expanded[negtags] 
#     # Get all the stop words
#     stopwords = get_bad_words()
# #    print all_words

    # Get all words to analyze frequency of unigrams and bigrams                                                                                                                                                                         
    all_words = [word for tag in word_tokens_byreviewid_expanded for word in word_tokens_byreviewid_expanded[tag]]
    # Get all the stop words                                                                                                                                                                                                             
    stopwords = get_bad_words()

#    dispersion_plot(all_words,postags)
    # Trigrams
    trigram_finder = TrigramCollocationFinder.from_words(all_words)
    trigram_finder.apply_ngram_filter(lambda w1, w2, w3: w1 in stopwords or w3 in stopwords)
    trigram_finder.apply_freq_filter(10)
    trigrams = trigram_finder.nbest(TrigramAssocMeasures.raw_freq, 2000)
    print "Number trigrams: %d" %len(trigrams)
#    print trigrams[:100]

    # Bigrams
    bigram_finder = BigramCollocationFinder.from_words(all_words)
    bigram_finder.apply_freq_filter(20)
    bigram_finder.apply_word_filter(lambda stopword: stopword in stopwords)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.raw_freq, 2000)
    print "Number bigrams: %d" %len(bigrams)
#    print bigrams[:100]

    # Unigrams
    word_freq_dist = DataFrame(dict(FreqDist(all_words)).items(), columns = ['word','count'])
    word_freq_dist = word_freq_dist[word_freq_dist['count'] > 20]
#    print word_freq_dist
    good_features = list(set(word_freq_dist['word']) - stopwords)
    print "Number unigrams: %d" %len(good_features)
    good_features.extend(bigrams)
    good_features.extend(trigrams)
#    print good_features

    # Output the features in the model
#    outfile =  args.folder+"/"+ args.folder+"_NB_sentiment.model.features.pyvar"
    outfile =  "NB_data/NB_sentiment.model.features.pyvar"
    outfile = open(outfile, 'w')
    pickle.dump(good_features, outfile)
    outfile.close()
    

    # Calculate the features
    negfeatures = [(get_sent_features(word_tokens_byreviewid_expanded[fid], good_features), 'neg') 
                   for fid in negtags]
    posfeatures = [(get_sent_features(word_tokens_byreviewid_expanded[fid], good_features), 'pos') 
                   for fid in postags]
#    print negfeatures

#     # Shuffle and balance the two classes
#     n_min = min([len(negfeatures), len(posfeatures)])
#     random.shuffle(negfeatures)
#     negfeatures = negfeatures[:n_min]
#     random.shuffle(posfeatures)
#     posfeatures = posfeatures[:n_min]

#     # Define training and testing data
#     numfolds = 10
#     foldsize = n_min/numfolds
#     negfolds = make_folds(negfeatures, foldsize)
#     posfolds = make_folds(posfeatures, foldsize)

    negfolds = cross_validation.StratifiedKFold(negfeatures, n_folds=10)
    print negfolds
    posfolds = cross_validation.StratifiedKFold(posfeatures, n_folds=10)
    print posfolds

    # 10 fold cross validation
    outfile = "NB_data/NB_sentiment.model.performance.tab"
    outfile = open(outfile, 'w')
    outfile.write("Fold\taccuracy\tpos_precision\tpos_recall\tneg_precision\tneg_recall\n")
    for fold in range(0, numfolds):
	outfile.write("%d\t" %fold)
	testdata = negfolds[fold] + posfolds[fold]
	traindata = []
	for i in range(0, numfolds):
	    if i != fold:
		traindata += negfolds[i]
		traindata += posfolds[i]
    	print 'train on %d instances, test on %d instances' % (len(traindata), len(testdata))

        result = eval_classifier(traindata, testdata)
        accuracy, posprecision, posrecall, negprecision, negrecall = result
        print  result
        outfile.write("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n"%(accuracy, posprecision, posrecall, negprecision, negrecall))
    outfile.close()

    # Save the classifier trained using all data
    classifier = NaiveBayesClassifier.train(negfeatures + posfeatures)
#    outfile = args.folder+"/"+ args.folder+"_NB_sentiment.model.pyvar" 
    outfile = "NB_data/NB_sentiment.model.pyvar" 
    outfile = open(outfile, 'w')
    pickle.dump(classifier, outfile)
    outfile.close()


if __name__ == "__main__":
    main()
