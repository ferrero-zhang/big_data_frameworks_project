from sklearn.ensemble import RandomForestClassifier

# read the data
pdf = pd.read_csv("test.csv", header=None)
X = pdf[pdf.columns[2:]]
y = pdf[1].astype(np.int)

# train the classifier
clf = RandomForestClassifier(n_estimators=200)
clf.fit(X.iloc[:1200000], y[:1200000])

# results
from sklearn.metrics import confusion_matrix, accuracy_score
confusion_matrix(res, y.iloc[1200000:])
# array([[75262, 19664, 15859,  4376],
#        [10915, 58641, 11104,  4704],
#        [ 7559,  2380, 19269,   983],
#        [  823,   368,   352,  1472]])
accuracy_score(res, y.iloc[1200000:])
# 0.6616323893706868

# save the classifier
from sklearn.externals import joblib
joblib.dump(clf, 'rfc_classifier.joblib')
