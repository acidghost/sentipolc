import random
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import LineTokenizer, RegexpTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.stem import SnowballStemmer
from processor import Processor as Proc

data_folder = './data'
encoding = 'UTF8'
language = 'italian'

wordTok = RegexpTokenizer(r'(\w+|@\w+|<3|(\:\-?\))|(\:\-?\()|(\;\-?\))|((\:|(X|x))\-?(D|d)))')
sentTok = LineTokenizer()
reader = CategorizedPlaintextCorpusReader(data_folder, r'SENTIPOLC-.*\.txt',
                                          cat_pattern=r'SENTIPOLC-(\w+)\.txt',
                                          encoding=encoding,
                                          word_tokenizer=wordTok,
                                          sent_tokenizer=sentTok)

pos_tweets = reader.sents(reader.fileids('pos'))
neg_tweets = reader.sents(reader.fileids('neg'))

# Inspection
rndP = random.randrange(len(pos_tweets))
rndN = random.randrange(len(neg_tweets))
print 'Pos:\n', pos_tweets[rndP:rndP+3], '\nNeg:\n', neg_tweets[rndN:rndN+3], '\n'

# All lowercase
pos_tweets = Proc.lowerize(pos_tweets)
neg_tweets = Proc.lowerize(neg_tweets)

# Removing digits
pos_tweets = Proc.remove_digits(pos_tweets)
neg_tweets = Proc.remove_digits(neg_tweets)

# Removing stopwords
swords = stopwords.words(language)
pos_tweets = Proc.remove_stopwords(pos_tweets, stopwords)
neg_tweets = Proc.remove_stopwords(neg_tweets, stopwords)

# Stemming
stemmer = SnowballStemmer(language)
pos_tweets = Proc.stem(pos_tweets, stemmer)
neg_tweets = Proc.stem(neg_tweets, stemmer)

# Inspection
print 'Pos:\n', pos_tweets[rndP:rndP+3], '\nNeg:\n', neg_tweets[rndN:rndN+3], '\n'

labeled_feats = {'pos': [], 'neg': []}
for postw in pos_tweets:
    labeled_feats['pos'].append(Proc.bag_of_words(postw))
for negtw in neg_tweets:
    labeled_feats['neg'].append(Proc.bag_of_words(negtw))

# Split for training and test data
train_data = []
test_data = []
for label in labeled_feats:
    cutoff = int(len(labeled_feats[label]) * 0.75)
    train_data.extend([(feat, label) for feat in labeled_feats[label][:cutoff]])
    test_data.extend([(feat, label) for feat in labeled_feats[label][cutoff:]])

print len(train_data), len(test_data)

classifier = NaiveBayesClassifier.train(train_data)
classifier.show_most_informative_features(n=30)

print 'Accuracy: ', accuracy(classifier, test_data)

sentences = [
    u'Oggi e una bella giornata'.encode(encoding),
    u'Ieri e stato molto difficile, ma soddisfacente!'.encode(encoding),
    u'La politica e molto noiosa...'.encode(encoding),
    u':)'.encode(encoding),
    u'Bellissimo'.encode(encoding)
]
for sent in sentences:
    lab = classifier.classify(Proc.bag_of_words(sent))
    print '"%s" classified as "%s"' % (sent, lab)
    print classifier.prob_classify(Proc.bag_of_words(sent)).prob('pos'), classifier.prob_classify(Proc.bag_of_words(sent)).prob('neg')
