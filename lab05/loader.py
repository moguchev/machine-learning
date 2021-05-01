import h5py
import pickle
import numpy as np

LAB_03 = 3
LAB_04 = 4


# Фичи из предыдущих лаб
def get_features_and_labels(lab_number: int):
    if lab_number == LAB_03:
        with h5py.File("./src/lab03/data.h5", 'r') as f:
            features = np.array(f['dataset_1'])
        with h5py.File("./src/lab03/labels.h5", 'r') as f:
            labels = np.array(f['dataset_1'])
    elif lab_number == LAB_04:
        features = pickle.load(open("./src/lab04/data.plk", 'rb'))
        labels = pickle.load(open("./src/lab04/titles.plk", 'rb'))
    else:
        features = labels = None

    return features, labels
