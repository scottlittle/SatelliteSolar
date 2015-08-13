import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train',categories=categories, shuffle=True, random_state=42)

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

import pickle
#vectorizer_pickle = pickle.dumps(count_vect)
pickle.dump(count_vect, open( "mornApp/data/my_vectorizer.pkl", "wb" ))
#model_pickle = pickle.dumps(clf)
pickle.dump(clf, open( "mornApp/data/my_model.pkl", "wb" ))
pickle.dump(tfidf_transformer, open( "mornApp/data/my_transformer.pkl", "wb" ))
#clf2 = pickle.loads(model_pickle)
clf2 = pickle.load(open( "mornApp/data/my_model.pkl", "rb" ) )
#count_vect2 = pickle.loads(vectorizer_pickle)
count_vect2 = pickle.load(open( "mornApp/data/my_vectorizer.pkl", "rb" ) )

docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect2.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf2.predict(X_new_tfidf)