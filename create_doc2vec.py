import gensim
import pandas as pd
import numpy as np

class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
        self.lines_error = 0
        self.lines_success = 0
        self.test = 0
    def __iter__(self):
        for line in open(self.filename):
            self.test += 1
            line_number, line = line.split(" ", 1)
            try:
                tag = cat_per_article.ix[pages_index.ix[int(line_number), 1]].values[0]
            except KeyError:
                self.lines_error += 1
                continue
            self.lines_success += 1
            yield gensim.models.doc2vec.LabeledSentence(
                words=line.split(), tags=[tag.values[0]])

sentences = LabeledLineSentence("frwiki_w_lines_wo_dbpedia_ok_small.txt")

import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

%%time
model = gensim.models.Doc2Vec(sentences, min_count=2, size=200, window=5, workers=16)
model.save("wiki_classifier.d2v")