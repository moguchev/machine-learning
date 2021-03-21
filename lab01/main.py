#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt


FILE_PATH = "./sources/API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_2056500.csv"
HEADER_INDEX = 2
YEARS_COLUMNS_INDEX = 4
TOP_AMOUNT = 5


if __name__ == '__main__':
    _, axes = plt.subplots(1, 2)

    # Parsing CSV file
    data_frame = pandas.read_csv(FILE_PATH, header=HEADER_INDEX)
    data_frame = data_frame.rename(data_frame.loc[data_frame.index]['Country Name'])
    data_frame = data_frame.drop(data_frame.columns[:YEARS_COLUMNS_INDEX], 1)
    data_frame.dropna(axis='columns', how='all', inplace=True)
    data_frame.dropna(axis='index', thresh=len(data_frame.columns), inplace=True)

    world_sum = data_frame.mean(axis='rows', numeric_only=True)
    world_sum.plot(
        ax=axes[0],
        xlabel='year',
        ylabel='%',
        grid=True,
        title='Access to electricity (% of population)'
    )

    top_fives_indexes = data_frame.mean(
        axis='columns',
        numeric_only=True,
        skipna=True
    ).sort_values(ascending=False)[:TOP_AMOUNT].index

    top_fives = data_frame.loc[top_fives_indexes].transpose()
    top_fives.plot(
        ax=axes[1],
        grid=True,
        xlabel='year',
        ylabel='%',
        title='Top 5 countries with access to electricity'
    )

    plt.show()




