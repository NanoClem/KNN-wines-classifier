# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle


# %%
def minkowski(a: list, b: list, p: int=1) -> float:
    """Compute the Minkowski distance between 2 data points.
    Note that data points should have the same dimension.

    Parameters
    -----
        a (list) -- First data point
        b (list) -- Second data point
        p (int) -- minkowski parameter (default: 1)
    
    Returns
    -----
        float -- Manhattan (p=1), Euclidian (p=2), ... distance between the two data points. 
    """
    dist = 0
    for i in range(len(a)):     # we assume a and b have the same dim
        dist += abs(a[i] - b[i])**p

    return dist**(1/p)


#%%
def knn(X_train, X_test, Y_train, k: int=3, p: int=1) -> list:
    """[summary]
    
    Parameters
    -----
        X_train ([type]) -- [description]
        Y_train ([type]) -- [description]
        X_test ([type]) -- [description]
        Y_test ([type]) -- [description]
        k (int) -- [description] (default: 3)
        p (int) -- [description] (default: 1)

    Returns
    -----
        list -- [description]
    """
    from collections import Counter
    predictions = []

    # Compute for each data point in the test set
    for test_point in X_test:
        distances = []

        for train_point in X_train:
            dist = minkowski(test_point, train_point, p=p)
            distances.append(dist)

        # Getting the k-nearest neighbours
        df_dists = pd.DataFrame(data=distances, columns=['distance'], index=Y_train.index)  # store distances in a DF
        df_nn    = df_dists.sort_values(by='distance')[:k]                        # sort distances and keep the k closest ones

        # Classify the data point
        counter = Counter(Y_train[df_nn.index])     # track labels of k nearest neighbours
        predict = counter.most_common()[0][0]       # get the most common label among neighbours
        predictions.append(predict)

    return predictions
# %%


if __name__ == "__main__":

    from sklearn.datasets import load_wine
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score

    # load the wine dataset
    wines = load_wine()
    data  = pd.DataFrame(data=wines.data, columns=wines.feature_names)
    data['target'] = wines.target

# %%
    # separating data and target
    X = data.drop('target', axis=1)
    Y = data.target
# %%
    # split data, 75% train / 25% test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=1, shuffle=True)
# %%
    # avoiding data leakage
    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)
# %%
    # compute KNN
    k = 5
    p = 2
    predictions = knn(X_train, X_test, Y_train, k, p)
# %%
    # computing accuracy of the model
    accuracy = accuracy_score(Y_test, predictions)
    print("KNN accuracy score : {}".format(accuracy))
# %%