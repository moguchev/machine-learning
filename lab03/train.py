import warnings
import h5py
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


warnings.filterwarnings('ignore')


def training(h5_data_file: str, h5_labels_file: str, n_estimators: int, random_state: int, test_size: float, scoring: str):
    # create all the machine learning models
    models = [('LR', LogisticRegression(random_state=random_state)),
              ('KNN', KNeighborsClassifier()),
              ('CART', DecisionTreeClassifier(random_state=random_state)),
              ('RF', RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)),
              ('NB', GaussianNB())]

    # variables to hold the results and names
    results = []
    names = []

    # import the feature vector and trained labels
    h5f_data = h5py.File(h5_data_file, 'r')
    h5f_label = h5py.File(h5_labels_file, 'r')

    global_features_string = h5f_data['dataset_1']
    global_labels_string = h5f_label['dataset_1']

    global_features = np.array(global_features_string)
    global_labels = np.array(global_labels_string)

    h5f_data.close()
    h5f_label.close()

    # verify the shape of the feature vector and labels
    print(f"[STATUS] features shape: {global_features.shape}")
    print(f"[STATUS] labels shape: {global_labels.shape}")

    print("[STATUS] training started...")

    # split the training and testing data
    (x_train, x_test, y_train, y_test) = train_test_split(np.array(global_features),
                                                          np.array(global_labels),
                                                          test_size=test_size,
                                                          random_state=random_state)

    print("[STATUS] separation train and test data...")
    print(f"Train data  : {x_train.shape}")
    print(f"Test data   : {x_test.shape}")
    print(f"Train labels: {y_train.shape}")
    print(f"Test labels : {y_test.shape}")

    # 10-fold cross validation
    for name, model in models:
        cv_results = cross_val_score(model, x_train, y_train, cv=10, scoring=scoring, n_jobs=-1)

        model.fit(x_train, y_train)
        print(classification_report(y_test, model.predict(x_test)))

        results.append(cv_results)
        names.append(name)
        print(f'{name}: {cv_results.mean()}')

    return names, results, x_train, y_train
