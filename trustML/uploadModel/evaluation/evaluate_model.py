from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
import numpy as np
import math
import random
import csv
import pandas as pd
import matplotlib.pyplot as plt



def get_model_and_data(model_file, data_file, label_file):
    model = joblib.load(model_file)
    data = np.genfromtxt(data_file, delimiter=",", dtype=float, missing_values=None)
    label = np.genfromtxt(label_file, delimiter=",", dtype=float, missing_values=None)

    return model, data, label


# clear the row includes empty data
def clear_missing_data(data):
    data = data[~np.isnan(data).any(axis=1)]
    return data


def get_result_round(data):
    data.sort()
    length = int(len(data) * 0.1)
    data[:length] = 2
    data[length:] = 4
    return data


# get a confusion matrix which will be used later
def get_confusion_matrix(model, data, label):
    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
    """
    :param model:
    :param data:
    :return: a confusion matrix with Y-axis as true label X-axis as predict label
    """
    my_model = model
    result = my_model.predict(data[:, :data.shape[1] - 1])
    # result = get_result_round(result)

    cm = confusion_matrix(data[:, data.shape[1] - 1], result, label)

    return cm


def get_precision_recall_accuracy(confusion_matrix):
    """
    :param confusion_matrix: get from sklearn package
    :return: precisions, recalls -> arrays, accuracy -> a float number
    """

    if confusion_matrix.shape[0] == 2:
        recall = np.zeros(1)
        precision = np.zeros(1)
        tp = confusion_matrix[0, 0]
        fp = confusion_matrix[1, 0]
        fn = confusion_matrix[0, 1]
        tn = confusion_matrix[1, 1]

        precision[0] = 0
        if tp + fp != 0:
            precision[0] = float(tp) / (tp + fp)

        recall[0] = 0
        if tp + fn != 0:
            recall[0] = float(tp) / (tp + fn)

        accuracy = 0
        if tp + fp + fn + tn != 0:
            accuracy = float(tp + tn) / (tp + fp + fn + tn)
    else:
        recall = np.zeros(confusion_matrix.shape[0])
        precision = np.zeros(confusion_matrix.shape[0])
        correctly_predicted = 0

        for row_idx in range(confusion_matrix.shape[0]):
            precision[row_idx] = float(confusion_matrix[row_idx][row_idx]) / np.sum(confusion_matrix[:, row_idx])
            recall[row_idx] = float(confusion_matrix[row_idx][row_idx]) / np.sum(confusion_matrix[row_idx, :])
            correctly_predicted += confusion_matrix[row_idx][row_idx]
        accuracy = correctly_predicted / np.sum(confusion_matrix)
    return precision, recall, accuracy


def get_test_model_accuracy(model, testingSet, label, split_data, split_model):
    with open('uncertainty_accuracy.csv', 'a') as f:
        writer = csv.writer(f)
        accset = []
        uncset = []
        for i in range(30):
            record = []
            data = get_data_portion(testingSet, split_model)
            data_uncertanity = int(float(get_uncertainty(model, data, label, split_data)) * 10000)
            uncset.append(data_uncertanity)
            record.append(data_uncertanity)
            cf = get_confusion_matrix(model, data, label)
            precision, recall, accuracy = get_precision_recall_accuracy(cf)
            record.append(int(accuracy * 10000))
            accset.append(int(accuracy * 10000))
            writer.writerow(record)
        return accset, uncset

    f.close()



def FindClosestPointDistance(trainingSet, testPoint, attrWeighting):
    minDist = 1000000000000;

    # Step through all the trainingSet data points
    for i in range(len(trainingSet)):
        thisDist = 0
        # For each attribute, add the weighted distance from the testPoint
        for j in range(len(testPoint)):
            thisDist += attrWeighting[j] * ((trainingSet[i][j] - testPoint[j]) ** 2)
        thisDist = math.sqrt(thisDist)
        # Find the training point with the minimum distance
        if (thisDist < minDist):
            minDist = thisDist
    return minDist


def getRandomTestSet(data):
    index = 5
    random.shuffle(data)
    division = len(data) / float(index)
    X_train = [data[int(round(division * i)): int(round(division * (i + 1)))] for i in range(index)]
    return X_train


def get_data_portion(data,size):
    s = int(len(data) * size)
    idx = np.random.randint(len(data), size=s)
    random_subset = data[idx, :]

    return random_subset


def get_model_uncertainty(model, testingSet, label):
    acc = []

    for i in range(10):
        cf = get_confusion_matrix(model, testingSet, label)
        print(cf)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        acc.append(accuracy)

    print("Model Uncertainty: " + str(np.std(acc)))


def get_uncertainty(model, testingSet, label, split_data):
    # X_train = getRandomTestSet(testingSet)
    acc = []

    for i in range(10):
        data = get_data_portion(testingSet, split_data)
        cf = get_confusion_matrix(model, data, label)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        acc.append(accuracy)

    print("Data Uncertainty: " + str(np.std(acc)))
    return str(np.std(acc))

#If the testing dataset contains missing data, the money given to user will be cut down based on sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(10 * (-x + 0.5)))


def get_missing_portion(testingSet):
    i = 0
    for row in testingSet:
        if np.isnan(row).any():
            i = i + 1

    return 1 - (i / testingSet.shape[0])


def get_similarity(trainingSet, testingSet, attrWeighting):
    # Check that they have the same number of attributes.
    if (len(trainingSet[0]) != len(testingSet[0])):
        print("Sets have different number of columns")
        return
    elif (len(trainingSet[0]) != len(attrWeighting)):
        print("Attribute weighting incorrect length")
        return

    # Normalise the data
    maxTrain = max(max(x) for x in trainingSet)
    maxTest = max(max(x) for x in testingSet)
    maxVal = max(maxTest, maxTrain)
    trainingSet *= 1 / maxVal
    testingSet *= 1 / maxVal

    # attrWeighting should sum to 1
    attrWeighting = [x * (1 / sum(attrWeighting)) for x in attrWeighting]

    totalDistance = 0

    # Evaluate the similarity using weighted KL-divergence
    for i in range(len(testingSet)):
        totalDistance += FindClosestPointDistance(trainingSet, testingSet[i], attrWeighting)

    averageDistance = totalDistance / len(testingSet)
    similarity = 1 - min(1, averageDistance)

    return similarity


# Weighting here is the importance of getting positive values correct, rather than negative values correct
def get_score(confusion_matrix, weighting, similarity):
    var = 0.3
    mean = 0.7
    a = 0.001
    multiplier = 100
    precision, recall, accuracy = get_precision_recall_accuracy(confusion_matrix)
    if confusion_matrix[0, 0] + confusion_matrix[1, 0] != 0:
        precisionN = float(confusion_matrix[0, 0]) / (confusion_matrix[0, 0] + confusion_matrix[1, 0])
    else:
        precisionN = 0

    if confusion_matrix[0, 0] + confusion_matrix[0, 1] != 0:
        recallN = float(confusion_matrix[0, 0]) / (confusion_matrix[0, 0] + confusion_matrix[0, 1])
    else:
        recallN = 0
    # Similarity is placed on a Gaussian distribution with the peak at 'mean' above.
    # This is so that datasets with moderate similarity rank highest.
    #       Such datasets have different enough data to be useful for testing
    #       Yet similar enough data that they are maximally applicable to the model
    similarityToValue = (1 / (math.sqrt(2 * math.pi * var))) * math.exp(-((similarity - mean) ** 2) / (2 * var))
    weightedAccuracy = 0.3 + recallN * (1 - weighting) + recall[0] * weighting
    weightedPrecision = 0.3 + precisionN * (1 - weighting) + precision[0] * weighting
    lengthToValue = 1.3 - 1 / (1 + a * np.sum(confusion_matrix))

    score = similarityToValue * lengthToValue * multiplier * weightedAccuracy * weightedPrecision
    return score

# get_score(get_confusion_matrix(model, [[0, 1, 0, 1], [1, 1, 1, 0]]),0.5,0.5)
