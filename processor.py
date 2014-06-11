__author__ = 'acidghost'

class Processor:

    @staticmethod
    def lowerize(sentences):
        for sent in sentences:
            for index in range(0, len(sent)):
                sent[index] = sent[index].lower()
        return sentences

    @staticmethod
    def remove_digits(sentences):
        for sent in sentences:
            for word in sent:
                for char in word:
                    if char.isdigit():
                        sent.remove(word)
                        break
        return sentences

    @staticmethod
    def remove_stopwords(sentences, stopwords):
        for sent in sentences:
            for word in sent:
                if word in stopwords.words():
                    sent.remove(word)
        return sentences

    @staticmethod
    def stem(sentences, stemmer):
        for sent in sentences:
            for index in range(len(sent)):
                sent[index] = stemmer.stem(sent[index])
        return sentences

    @staticmethod
    def bag_of_words(sent):
        dict = {}
        for word in sent:
            dict[word] = True
        return dict