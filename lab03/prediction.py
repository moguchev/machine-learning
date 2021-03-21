import matplotlib.pyplot as plt
import glob
import cv2
from sklearn.ensemble import RandomForestClassifier
from features import get_feature

DEF_SIZE = tuple((500, 500))


def display(image, title, path):
    fig = plt.figure()
    fig.suptitle(title)
    plt.axis('off')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.savefig(path)


def predict(train_data, train_labels, test_path, labels, result_path, n_estimators, random_state, fixed_size=DEF_SIZE):
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, n_jobs=-1)

    clf.fit(train_data, train_labels)

    # loop through the test images
    for ind, file in enumerate(glob.glob(test_path + "/*.*")):
        # read the image
        image = cv2.imread(file)
        image = cv2.resize(image, fixed_size)

        # get feature
        global_feature = get_feature(image)

        # predict label of test image
        prediction = clf.predict(global_feature.reshape(1, -1))[0]

        # display the output image
        display(image, labels[prediction], f'{result_path}/{ind}.png')
