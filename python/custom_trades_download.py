import os
from utility import download_file, get_all_symbols, get_parser, get_start_end_date_objects, convert_to_date_object, \
    get_path
import sys
from datetime import *
from enums import YEARS, MONTHS, START_DATE, END_DATE, PERIOD_START_DATE
import pandas as pd


def custom_monthly_trades(trading_type, symbols, num_symbols, years, months, start_date, end_date, folder, checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download monthly {} trades ".format(current + 1, num_symbols, symbol))
        for year in years:
            for month in months:
                current_date = convert_to_date_object('{}-{}-01'.format(year, month))
                if start_date <= current_date <= end_date:
                    path = get_path(trading_type, "trades", "monthly", symbol)
                    file_name = "{}-trades-{}-{}.zip".format(symbol.upper(), year, '{:02d}'.format(month))
                    download_file(path, file_name, date_range, folder)

                    if checksum == 1:
                        checksum_path = get_path(trading_type, "trades", "monthly", symbol)
                        checksum_file_name = "{}-trades-{}-{}.zip.CHECKSUM".format(symbol.upper(), year,
                                                                                   '{:02d}'.format(month))
                        download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


monthly = True
daily = True
futures = True
PATH_FOLDER = "E:\\data\\binance_data\\data"
if futures:
    PATH_FOLDER = os.path.join(PATH_FOLDER, "futures")
sub_folders = [x[0] for x in os.walk(PATH_FOLDER)]
market_types = ["um", "cm"]

for market_type in market_types:
    symbols = get_all_symbols(market_type)
    num_symbols = len(symbols)

    period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
        PERIOD_START_DATE)
    dates = pd.date_range(end=datetime.today(), periods=period.days + 1).to_pydatetime().tolist()
    dates = [date.strftime("%Y-%m-%d") for date in dates]

    # Monthly trades
    if monthly:
        monthly_paths = [x[0] for x in os.walk(os.path.join(PATH_FOLDER, market_type, "monthly", "trades"))]

    print("End of loop!")

print("End of script!")
