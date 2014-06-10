import csv

from tweet import Tweet

from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import LineTokenizer, RegexpTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

with open('data/SENTIPOLC-Evalita-2014.csv', 'r') as csvfile:
    csvReader = csv.reader(csvfile)
    lines = [row for row in csvReader]

# Remove header line
lines = lines[1:]

# Compose tweets array
tweets = []
for line in lines:
    # Skip if tweet is not available
    if str(line[6]).startswith('Tweet Not Available'):
        continue
    tw = Tweet(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
    tweets.append(tw)

pos_tweets = []
neg_tweets = []
for tweet in tweets:
    if tweet.opinion > 0:
        pos_tweets.append(tweet)
    elif tweet.opinion < 0:
        neg_tweets.append(tweet)

print 'Pos: %s\nNeg: %s\n' % (len(pos_tweets), len(neg_tweets))

# Saving positive tweets into a file
with open('data/SENTIPOLC-pos.txt', 'w') as posfile:
    posfile.writelines('\n'.join([tweet.text for tweet in pos_tweets]))
    posfile.close()

# Saving negative tweets into another file
with open('data/SENTIPOLC-neg.txt', 'w') as negfile:
    negfile.writelines('\n'.join([tweet.text for tweet in neg_tweets]))
    negfile.close()

wordTok = RegexpTokenizer(r'\w+|(@\w+)|(<3)|(\:\))|(\:\()|(\;\))|(\:D)')
lineTok = LineTokenizer()
reader = CategorizedPlaintextCorpusReader('./data', r'SENTIPOLC-.*\.txt',
                                          cat_pattern=r'SENTIPOLC-(\w+)\.txt',
                                          #encoding='utf8',
                                          word_tokenizer=wordTok,
                                          sent_tokenizer=lineTok)
print 'Categories: %s\n' % (reader.categories())

pos_tweets = reader.sents(reader.fileids('pos'))
neg_tweets = reader.sents(reader.fileids('neg'))

print 'Pos:\n', pos_tweets[:3], '\n\nNeg:\n', neg_tweets[:3]

# All lowercase
for sent in pos_tweets + neg_tweets:
    for index in range(0, len(sent)):
        sent[index] = sent[index].lower()

# Removing stopwords
swords = stopwords.words('italian')
for sent in pos_tweets + neg_tweets:
    for word in sent:
        if word in swords:
            sent.remove(word)

print 'Pos:\n', pos_tweets[:3], '\n\nNeg:\n', neg_tweets[:3]

def bag_of_words(sent):
    dict = {}
    for word in sent:
        dict[word] = True
    return dict

labeled_feats = {'pos': [], 'neg': []}
for postw in pos_tweets:
    labeled_feats['pos'].append(bag_of_words(postw))
for negtw in neg_tweets:
    labeled_feats['neg'].append(bag_of_words(negtw))

# Split for training and test data
train_data = []
test_data = []
for label in labeled_feats:
    cutoff = int(len(labeled_feats[label]) * 0.75)
    train_data.extend([(feat, label) for feat in labeled_feats[label][:cutoff]])
    test_data.extend([(feat, label) for feat in labeled_feats[label][:-cutoff]])

print len(train_data), len(test_data)

classifier = NaiveBayesClassifier.train(train_data)
print '20 most informative features:\n'
for word, t in classifier.most_informative_features(n=20):
    print word
print 'Accuracy: ', accuracy(classifier, test_data)
