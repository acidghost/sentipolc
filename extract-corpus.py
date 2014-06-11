__author__ = 'acidghost'

import csv

from tweet import Tweet


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