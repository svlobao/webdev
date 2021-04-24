# Importing libs
# Importando bibliotecas
# ライブラリのインポート

import pandas
import numpy as np
import requests
from datetime import datetime
from dateutil.rrule import rrule, DAILY
import logging

# ---------------- # ---------------- # ---------------- # ---------------- # ---------------- #

# API root and request URL example
# Corpo genérico da API e um exemplo de URL
# APIリクエストの例

# api_root = 'https://api.ratesapi.io/api/'

# Example: This is a sample of how we're gonna request info from specific dates, e.g. Apr/15/2021
# Exemplo: Este é um exemplo de como vamos requisitar informações do dia 15/Abril/2021
# 'https://api.ratesapi.io/api/2021-04-15'
# 例: これが２０２１年４月１５日のデータのリクエストするの例


# ---------------- # ---------------- # ---------------- # ---------------- # ---------------- #


logging.info(msg='Initializing historical data collection.')


def load_historical_data(api_root, start_date, end_date, create_csv=False, output_file_path='', file_name=''):
    """ No need to input '.csv' in your file name. Output file path should receive directory paths with doubled
    counter slash, instead of only one.'"""

    all_keys = []
    all_dates = pandas.date_range(start_date, end_date, freq='B')

    # Iterate through all dates between 1999-01-04 and today
    # Passar por todas as datas entre 1999-01-04 e hoje
    # 1999-01-04から今日までの全ての日付を通します

    logging.info(msg='Collecting data...\n\nProgress:\n')

    count_1 = 0
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        print(f'\n{count_1} / {len(all_dates)}\t{round(100*count_1 / len(all_dates), 1)}%')
        # No weekends, because there are no currency fluctuarion data
        # Sem finais de semana, pq nao tem dados referente a flutuacao monetaria
        # 通貨変動データがありませんので、週末はパスです
        if datetime.weekday(dt) < 5:
            # Call API data for each date
            # Requisitar dados da API para cada data
            # 日付ごとにAPIのデータをリクエストする
            response = requests.get(api_root + str(dt)[0:10])
            json_obj = response.json()

            for _key in json_obj['rates'].keys():
                if _key not in all_keys:
                    all_keys.append(_key)

            count_1 += 1

    logging.info(msg='\nColumns collection was a success!\n')

    df = pandas.DataFrame(columns=all_keys, index=all_dates)

    logging.info(msg='\nDataFrame created with collected columns.\n')
    logging.info(msg='\nInitializing data input...\n\nProgress:\n\n')

    count_2 = 0
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        print(f'\n{count_2} / {len(all_dates)}\t{round(100*count_2 / len(all_dates), 1)}%')
        if datetime.weekday(dt) < 5:
            response = requests.get('https://api.ratesapi.io/api/' + str(dt)[0:10])
            json_obj = response.json()

            for _key in json_obj['rates'].keys():
                df.loc[[str(dt)[0:10]], [_key]] = json_obj['rates'][_key]

            # Progress tracking while compiling
            count_2 += 1

    logging.info(msg='\nData input was a success!\n')
    df_fill = df.replace(np.nan, 0)
    logging.info(msg='\nFilled NaN values with 0\n')

    # If user wants to create a CSV file
    # Se o usuário quiser criar um arquivo CSV
    # もしクライアントがCSVファイルを生成したいのなら
    if create_csv:
        file_extension = '.csv'
        df_fill.to_csv(output_file_path + file_name + file_extension)
        logging.info(f'\nCSV file created on: {output_file_path + file_name + file_extension}\n')

    logging.info(msg='\nProcess finished.\n')

    return df_fill
