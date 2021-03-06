import os
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from datetime import date


def words2lists(filename):

    lists = []
    file = open(filename, "r", encoding="utf-8")
    while True:
        line = file.readline().rstrip("\n")
        if line:
            lists.append(line)
        else:
            break
    return lists


def csv2list(filename):

    lists = []
    file = open(filename, "r", encoding="utf-8")
    while True:
        line = file.readline().rstrip("\n")
        if line:
            line = line.split("`")
            lists.append(line)
        else:
            break
    return lists


def sentimentalize(words):

    poslen = len(POSITIVE_WORDS.intersection(words))
    neglen = len(NEGATIVE_WORDS.intersection(words))

    if poslen > 0 and neglen == 0:
        return POSITIVE
    elif poslen == 0 and neglen > 0:
        return NEGATIVE
    elif poslen > 0 and neglen > 0:
        return BOTH
    else:
        return UNKNOWN


def count_sentiment(sentences):

    sents = Counter()
    words = Counter()

    for sentence in sentences:
        sentiment = sentimentalize(sentence)
        sents[sentiment] += 1
        words[sentiment] += len(sentence)

    return sents, words


def parse_sentiment(text):

    sentences = [
        [word.lower() for word in nltk.word_tokenize(sentence)]
        for sentence in nltk.sent_tokenize(text)
    ]
    sents, words = count_sentiment(sentences)
    total = sum(words.values())

    for sentiment, count in words.items():
        pcent = (count / total) * 100
        nsents = sents[sentiment]
        # print("{:0.3f}% {} ({} sentences)".format(pcent, sentiment, nsents))
    return sentiment


def parse_data(data):

    result = []
    for item in data:
        sentiment = parse_sentiment(item[1])
        # tweet_date = date.fromisoformat(item[0])
        result.append([
            # tweet_date.year, tweet_date.month, tweet_date.day,
            item[0], sentiment])
    return result


POSITIVE_WORDS_DIR = os.path.join('feature_words', 'positive-words.txt')
NEGATIVE_WORDS_DIR = os.path.join('feature_words', 'negative-words.txt')
CRAWLED_DATA_DIR = os.path.join('crawled_data.csv')
POSITIVE = 'positive'
NEGATIVE = 'negative'
UNKNOWN = 'unknown'
BOTH = 'both'
POSITIVE_WORDS = set(words2lists(POSITIVE_WORDS_DIR))
NEGATIVE_WORDS = set(words2lists(NEGATIVE_WORDS_DIR))


if __name__ == "__main__":
    results = []
    count_pos = 0
    count_neg = 0
    count_unkn = 0
    count_both = 0
    data = csv2list(CRAWLED_DATA_DIR)
    results = parse_data(data)

    for result in results:
        if(result[1] is 'positive'):
            count_pos += 1
        elif(result[1] is 'negative'):
            count_neg += 1
        elif(result[1] is 'unknown'):
            count_unkn += 1
        elif(result[1] is 'both'):
            count_both += 1

    print("positive tweets: {:0.3f}% ".format(count_pos/len(results)*100))
    print("negative tweets: {:0.3f}% ".format(count_neg/len(results)*100))
    print("unknown tweets: {:0.3f}% ".format(count_unkn/len(results)*100))
    print("both tweets: {:0.3f}% ".format(count_both/len(results)*100))
