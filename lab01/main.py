#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt
import numpy

FILE_PATH = "./sources/API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_2056500.csv"
HEADER_INDEX = 2
YEARS_COLUMNS_INDEX = 4
TOP_AMOUNT = 5

# # World data
# def plot_world():
#     x = list(map(int, frame.columns.values.tolist()[4:]))  # years
#     y = frame.iloc[:, 4:].sum().tolist()  # world sum by year
#     plt.plot(x, y)
#     plt.xticks(x, x, rotation="vertical")
#
#
# # Top-5 countries data
# def plot_top():
#     for idx in (frame.sum(axis=1)).sort_values(ascending=False)[:5].index.tolist():  # top-5 indexes
#         plt.plot(frame.columns.values.tolist()[4:], frame.iloc[idx, 4:].tolist(), label=frame.iloc[idx, 0])
#     plt.xticks(rotation="vertical")
#     plt.legend()

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]


if __name__ == '__main__':
    # Parsing CSV file and set 0 if NaN
    data_frame = pandas.read_csv(FILE_PATH, header=HEADER_INDEX).fillna(0)
    data_frame = data_frame.drop(data_frame.columns[1:YEARS_COLUMNS_INDEX], 1)

    world_sum = data_frame.mean(axis='rows', numeric_only=True, skipna=True)
    world_sum = numpy.trim_zeros(world_sum, trim='fb')
    world_sum.plot(title='Access to electricity (% of population)').get_figure().show()
    plt.show()

    top_fives_indexes = data_frame.mean(
        axis='columns',
        numeric_only=True,
        skipna=True
    ).sort_values(ascending=False)[:TOP_AMOUNT].index.tolist()

    print(data_frame)

    for idx in top_fives_indexes:
        country_name = data_frame.iloc[idx, 0]
        years = data_frame.columns.values.tolist()[1:]
        values = data_frame.iloc[idx, 1:].tolist()

        plt.plot(
            years,
            zero_to_nan(values),
            label=country_name,
            alpha=0.5,
        )
        plt.title('TOP 5 Countries with access to electricity (% of population)')
        plt.legend(loc='best')
        plt.xticks(rotation="vertical")
        print(data_frame.iloc[idx, 0])
    plt.show()




