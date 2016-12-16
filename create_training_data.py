import gensim
import pandas as pd
import numpy as np

tag_numbers = {
    'priority_Sciences': 0,
    'priority_Vie_humaine': 1,
    'priority_Espace': 2,
    'priority_Nature': 3,
}

def get_tag_for_line_number(line_number):
    try:
        return cat_per_article.ix[pages_index.ix[int(line_number), 1]].values[0]
    except KeyError:
        return ""

def remove_null(line):
    split = line.split(" ", 1)
    if len(split) > 1:
        return split[1]
    return ""

# get the data
cat_per_article = pd.read_csv("wiki2vec-master/data/cat_per_article.csv", header=None)
cat_per_article = cat_per_article.set_index(0, drop=True)
pages_index = pd.read_csv("wiki2vec-master/data/seded_index.txt", sep="#", header=None)
model = gensim.models.Doc2Vec.load("wiki_classifier/wiki_classifier.d2v")

# create training data
lines = sc.textFile("wiki2vec-master/data/small.corpus")
lines = lines.map(lambda line: line.split(" ", 1))
lines = lines.map(lambda (n, line): (get_tag_for_line_number(int(n)), remove_null(line)))
lines = lines.filter(lambda (tag, line): bool(tag))
lines = lines.map(lambda (tag, line): (tag_numbers[tag], re.sub("DBPEDIA_ID\/[^ ]* ", '', line)))
lines = lines.map(lambda (tag_number, line): (tag_number, model.infer_vector(line.split())))
# libsvm format
lines = lines.map(lambda (tag_number, vector): ("{}{}".format(tag_number, " ".join(["{}:{}".format(i, value) for i, value in enumerate(vector)])))
res = lines.collect()