#
# Developer: Sandro Vianna Lobao
# Date: April/8/2021
#
# Title: Get currency history and generate a CSV file from it.
#
# ---------------- # ---------------- # ---------------- # ---------------- # ---------------- #


from get_historical_data import load_historical_data
from datetime import datetime, date


if __name__ == '__main__':
    dt_today = datetime.today()
    today = str(dt_today)[0:10]

    this_year = int(today[0:4])

    if int(today[5:7]) < 10:
        this_month = int(today[6])
    else:
        this_month = int(today[5:7])

    if int(today[8:10]) < 10:
        this_day = int(today[9])
    else:
        this_day = int(today[8:10])

    end_date = date(this_year, this_month, this_day)

    start_date = date(1999, 1, 4)

    df = load_historical_data(
        'https://api.ratesapi.io/api/',
        start_date,
        end_date,
        True,
        'C:\\Users\\svlob\\Desktop\\',
        'Currency - Modularizada')
