class Tweet:
    def __init__(self, id, subj, pos, neg, iro, top, text):
        self.id = id
        self.subj = True if int(subj) == 1 else False
        self.opinion = (1 if int(pos) == 1 else (-1 if int(neg) == 1 else 0))
        self.iro = True if int(iro) == 1 else False
        self.top = top
        self.text = text

    def __str__(self):
        return ', '.join([self.id, self.subj, self.opinion, self.iro, self.top, self.text])
