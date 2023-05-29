import cv2
from skimage.feature import greycomatrix, greycoprops
from skimage.measure import shannon_entropy
import skimage
import numpy as np
import joblib
import random
import sklearn
import pickle
from collections import Counter
# from dill import dumps, loads
# import dill

def contrastStretching(image):
    min, max = np.percentile(image, (4,96))
    image_cs = skimage.img_as_ubyte(skimage.exposure.rescale_intensity(image, in_range=(min, max)))
    return image_cs

def glcm(image):
    properties = ['energy', 'contrast', 'correlation', 'homogeneity', 'entropy']
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    features = []

    for angle in angles :
        glcm = greycomatrix(image, distances=[1], angles = [angle])
        for prop in properties :
            if prop == 'entropy' :
                features.append(shannon_entropy(glcm))
            else :
                features.append((greycoprops(glcm, prop))[0,0])

    return features

class Node:
    def __init__(self, feature=None, threshold=None, data_left=None, data_right=None, gain=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.data_left = data_left
        self.data_right = data_right
        self.gain = gain
        self.value = value

class DecisionTree:
    def __init__(self, min_samples_split=2):
        self.min_samples_split = min_samples_split
        self.root = None

    @staticmethod
    def _entropy(s):
        counts = np.bincount(np.array(s, dtype=np.int64))
        probability = counts / len(s)

        entropy = 0
        for pi in probability:
            if pi > 0:
                entropy += pi * np.log2(pi)
        return -entropy

    def _information_gain(self, parent, left_child, right_child):
        num_left = len(left_child) / len(parent)
        num_right = len(right_child) / len(parent)
        return self._entropy(parent) - (num_left * self._entropy(left_child) + num_right * self._entropy(right_child))

    def _best_split(self, X, y):
        best_split = {}
        best_info_gain = -1
        n_rows, n_cols = X.shape

        for f_idx in range(n_cols):
            X_curr = X[:, f_idx]

            for threshold in np.unique(X_curr):
                df = np.concatenate((X, y.reshape(-1, 1)), axis=1)
                df_left = np.array([row for row in df if row[f_idx] <= threshold])
                df_right = np.array([row for row in df if row[f_idx] > threshold])

                if len(df_left) > 0 and len(df_right) > 0:
                    y = df[:, -1]
                    y_left = df_left[:, -1]
                    y_right = df_right[:, -1]

                    gain = self._information_gain(y, y_left, y_right)
                    if gain > best_info_gain:
                        best_split = {
                            'feature_index': f_idx,
                            'threshold': threshold,
                            'df_left': df_left,
                            'df_right': df_right,
                            'gain': gain
                        }
                        best_info_gain = gain
        return best_split

    def _build(self, X, y):
        n_rows, n_cols = X.shape

        if n_rows >= self.min_samples_split:
            best = self._best_split(X, y)
            if best['gain'] > 0:
                left = self._build(
                    X=best['df_left'][:, :-1],
                    y=best['df_left'][:, -1],
                )
                right = self._build(
                    X=best['df_right'][:, :-1],
                    y=best['df_right'][:, -1],
                )

                return Node(
                    feature=best['feature_index'],
                    threshold=best['threshold'],
                    data_left=left,
                    data_right=right,
                    gain=best['gain']
                )
        return Node(
            value=Counter(y).most_common(1)[0][0]
        )

    def fit(self, X, y):
        self.root = self._build(X, y)

    def _predict(self, x, tree):
        if tree.value != None:
            return tree.value

        feature_value = x[tree.feature]

        if feature_value <= tree.threshold:
            return self._predict(x=x, tree=tree.data_left)
        if feature_value > tree.threshold:
            return self._predict(x=x, tree=tree.data_right)

    def predict(self, X):
        return [self._predict(x, self.root) for x in X]

class RandomForest:
    def __init__(self, num_trees, min_samples_split=2):
        self.num_trees = num_trees
        self.min_samples_split = min_samples_split
        self.decision_trees = []

    @staticmethod
    def _sample(X, y):
        n_rows, n_cols = X.shape
        samples = np.random.choice(a=n_rows, size=n_rows, replace=True)
        return X[samples], y[samples]

    def fit(self, X, y):
        num_built = 0
        while num_built < self.num_trees:
            try:
                clf = DecisionTree(min_samples_split=self.min_samples_split)
                _X, _y = self._sample(X, y)
                clf.fit(_X, _y)
                self.decision_trees.append(clf)
                num_built += 1
            except Exception as e:
                continue

    def predict(self, X):
        y = []
        for tree in self.decision_trees:
            y.append(tree.predict(X))

        y = np.swapaxes(a=y, axis1=0, axis2=1)

        predictions = []
        for preds in y:
             predictions.append(Counter(preds).most_common(1)[0][0])
        return round(predictions[0])


