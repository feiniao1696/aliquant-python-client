import numpy as np
import pandas as pd
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys

def read_result_from_log(log_file):
    fileIn = open(log_file, "r")
    is_wanted_line = 0
    data_dict = {}
    while 1:
        line = fileIn.readline()
        if not line:
            break
        if "strategy_backtesting_history_data" in line:
            is_wanted_line = 1
        if is_wanted_line == 1 and len(line.split(",")) >= 6:
            data_line = line.strip("\n").split("\t")[2]
            data_line_list = data_line.split(",")
            data_dict[data_line_list[0]] = [data_line_list[1], data_line_list[2], data_line_list[3], data_line_list[4]]
    return data_dict

def plot_backtest_result_curve(log_file):
    data_dict = read_result_from_log(log_file)
    #benchmark_dates, benchmark_value = sort_dict_buy_key(data_dict)
    portfolio_history_data = pd.DataFrame(data_dict).T
    portfolio_history_data.columns = ['total_value', 'cash', 'stock_value', 'bench_value']

    dates_ = list(portfolio_history_data.index)
    dates = []
    for d in dates_:
        if d == None: 
            d = config.start_date
        date = datetime.datetime.strptime(d, '%Y-%m-%d').date() 
        dates.append(date)
    #dates = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in dates if d != None else config.start_date]

    total_value = list(portfolio_history_data["total_value"].values)
    cash = list(portfolio_history_data["cash"].values)
    cash_value = list(portfolio_history_data["stock_value"].values)
    bench_value = list(portfolio_history_data["bench_value"].values)

    
    # xaxis tick formatter
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # xaxis ticks
    #plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    # figure title and legend
    plt.gca().legend()
    plt.gca().set(title="event factor backtesting porfolio value",
                  ylabel = "porfolio total value",
                  xlabel = "backtesting time")
    plt.locator_params(axis='x', nticks=10)
    plt.plot(dates, total_value)
    plt.plot(dates, bench_value)
    plt.gcf().autofmt_xdate()
    plt.show()

#data = read_result_from_log(sys.argv[1])
#plot_backtest_result_curve(data)
