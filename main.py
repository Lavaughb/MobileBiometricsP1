''' Imports '''
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import get_images
import get_landmarks
import performance_plots

from sklearn.multiclass import OneVsRestClassifier as ORC
from sklearn.model_selection import train_test_split
import pandas as pd

''' Import classifier '''
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.svm import SVC

''' Load the data and their labels '''
image_directory = '/Users/nicolasngwai/Downloads/projectDatabase/Project1Database'
#X, y = get_images.get_images(image_directory)
Q, w = get_images.get_images_dark(image_directory)
A, b = get_images.get_images_light(image_directory)

''' Get distances between face landmarks in the images '''
#X, y = get_landmarks.get_landmarks(X, y, 'landmarks/', 68, False)
A, b = get_landmarks.get_landmarks(A, b, 'landmarks/', 68, False)
Q, w = get_landmarks.get_landmarks(Q, w, 'landmarks/', 68, False)

''' Matching and Decision '''
clf = ORC(SVC(gamma='auto',probability=True))
#clf = ORC(knn())
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
#clf.fit(X_train, y_train)
clf.fit(A, b)

matching_scores = clf.predict_proba(Q)

gen_scores = []
imp_scores = []
classes = clf.classes_
matching_scores = pd.DataFrame(matching_scores, columns=classes)

for i in range(len(w)):    
    scores = matching_scores.loc[i]
    mask = scores.index.isin([w[i]])
    gen_scores.extend(scores[mask])
    imp_scores.extend(scores[~mask])
    

performance_plots.performance(gen_scores, imp_scores, 'kNN', 500)


