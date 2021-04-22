from sklearn import decomposition
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

data = ['gpu processor cpu performance',
        'gpu performance ram computer',
        'cpu computer ram processor jeans']
tf = TfidfVectorizer(max_features=None).fit(data)
# tf.vocabulary_.__len__()  # returns 7 as we passed 7 words
data = tf.fit_transform(data)  # returns 3x7 sparse matrix
print(data.shape)
print(data)
data = data.toarray()
pca = decomposition.PCA(
        n_components=3,
        whiten=False,
        svd_solver='auto'
    )

newData = pca.fit_transform(data)

print(data.shape)
print(newData.shape)