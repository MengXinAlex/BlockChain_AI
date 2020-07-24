import numpy as np
from sklearn import preprocessing
def generate_from_data(file_path):
    data = np.genfromtxt(file_path, dtype=None, encoding='UTF-8', names=True, delimiter=',')
    encoder = preprocessing.LabelEncoder()
    encoder.fit(data['diagnosis'])
    diagnosis = encoder.transform(data['diagnosis']).astype(int)
    new_data = diagnosis.reshape(-1, 1)
    for i in range(2, len(data.dtype.names)):
        new_data = np.concatenate((new_data, np.expand_dims(data[data.dtype.names[i]], axis=0).T), axis=1)
    scale_data = preprocessing.scale(new_data[:, 1:])

