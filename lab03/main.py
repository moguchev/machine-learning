import os
from prepare import init_h5py
from train import training
from prediction import predict
import yaml
import argparse
import matplotlib.pyplot as plt

CFG_PATH = './config.yaml'


def save_results(file_path: str, r_names: list, r_results: list):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    fig = plt.figure()
    fig.suptitle('Machine Learning algorithm comparison')
    ax = fig.add_subplot(111)

    plt.boxplot(r_results)
    ax.set_xticklabels(r_names)

    plt.savefig(f'{file_path}/result.png')


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, help="path to config yaml")
    args = vars(parser.parse_args())

    config = args.get('-c') if args.get('-c') else CFG_PATH

    with open(config) as file:
        cfg_data = yaml.load(file, Loader=yaml.FullLoader)

    return cfg_data


if __name__ == "__main__":
    cfg = get_config()

    train_dir = cfg.get('train_dir_path')
    test_dir = cfg.get('test_dir_path')
    result_path = cfg.get('result_dir_path')
    h5_labels_file = cfg.get('h5_labels')
    h5_data_file = cfg.get('h5_data')
    n_estimators = cfg.get('trees_number')
    random_state = cfg.get('seed')
    test_size = cfg.get('test_size')
    scoring = cfg.get('scoring')

    labels = os.listdir(train_dir)
    labels.sort()

    init_h5py(
        h5_labels_file=h5_labels_file,
        h5_data_file=h5_data_file,
        train_path=train_dir,
        train_labels=labels,
    )

    names, results, x_train, y_train = training(
        h5_labels_file=h5_labels_file,
        h5_data_file=h5_data_file,
        n_estimators=n_estimators,
        random_state=random_state,
        test_size=test_size,
        scoring=scoring,
    )

    save_results(result_path, names, results)

    predict(x_train, y_train, test_dir, labels, result_path, n_estimators, random_state)
