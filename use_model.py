from sklearn.externals import joblib
import Stemmer
import gensim

labels = {
    0: 'priority_Sciences',
    1: 'priority_Vie_humaine',
    2: 'priority_Espace',
    3: 'priority_Nature',
}

# load the classifier
rfc_clf = joblib.load("rfc_classifier.joblib")
# load the stemmer
stemmer = Stemmer.Stemmer('french')
# load the Doc2Vec model
model = gensim.models.Doc2Vec.load("wiki_classifier/wiki_classifier.d2v")

# example document
sentence = 'bonjour bienvenue chez moi'

# stem the sentence
stemmed_sentence = stemmer.stemWords(sentence.split())

# corresponding vector
vector = model.infer_vector(stemmed_sentence)

# get the predicted class
prediction = rfc_clf.predict(vector.reshape(1, -1))
# the category corresponding to the prediction
print(labels[prediction])
