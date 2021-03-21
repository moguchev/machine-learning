from sklearn.preprocessing import LabelEncoder
from features import get_feature
import numpy as np
import cv2
import os
import h5py


DEF_SIZE = tuple((500, 500))


def init_h5py(train_path: str, train_labels: list[str], h5_data_file: str, h5_labels_file: str, fixed_img_size=DEF_SIZE):
    global_features = []
    labels = []

    # loop over the training data sub-folders
    for training_name in train_labels:
        current_dir = os.path.join(train_path, training_name)

        images = [f for f in os.listdir(current_dir) if
                  os.path.isfile(os.path.join(current_dir, f)) and f.endswith(".jpg") or f.endswith(".png")]

        for file in images:
            file_path = os.path.join(current_dir, file)

            # read the image and resize it to a fixed-size
            image = cv2.imread(file_path)
            image = cv2.resize(image, fixed_img_size)

            global_feature = get_feature(image)

            # update the list of labels and feature vectors
            labels.append(training_name)
            global_features.append(global_feature)

        print(f"[STATUS] processed folder: {training_name}")

    le = LabelEncoder()
    target = le.fit_transform(labels)

    # save the feature vector using HDF5
    h5f_data = h5py.File(h5_data_file, 'w')
    h5f_data.create_dataset('dataset_1', data=np.array(global_features))

    h5f_label = h5py.File(h5_labels_file, 'w')
    h5f_label.create_dataset('dataset_1', data=np.array(target))

    h5f_data.close()
    h5f_label.close()

    print("[STATUS] end of training..")
