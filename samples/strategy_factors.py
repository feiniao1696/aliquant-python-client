import math
import pandas as pd
from aliquant.runner import *

def initilize(context):
    context.codes = ['600276.SH', '600479.SH', '002349.SZ', '000915.SZ', '300233.SZ', '300006.SZ', '600085.SH', '002365.SZ']
    set_stock_pool(context.codes)

    # set backtesting parameters
    set_commission(0.002)
    context.last_trade_month = None

def get_stock_fundamental_data():
    q1 = query(SEC.code, SEC.market_val, SEC.trade_market_val, SEC.pb, SEC.pe, SEC.ps).filter(Filter(SEC.code).isIn(context.codes))
    context.fundamental_data = get_fundamentals(q1)

def get_trading_codes():
    code_set1 = set(context.codes)
    code_set2 = set(context.fundamental_data["code"].values)
    return code_set1 & code_set2

def is_trading_day(bars):
    current_date = config.getStrDate(bars.getDateTime())
    current_month = current_date[0:7]
    if context.last_trade_month == None:
        context.last_trade_month = current_month
        return True
    elif current_month == context.last_trade_month:
        return False
    else:
        context.last_trade_month = current_month
        return True

def get_top_stocks():
    tradable_codes = get_trading_codes()
    tradable_codes_data = context.fundamental_data[context.fundamental_data['code'].isin(tradable_codes)]
    sorted_tradable_codes_data = tradable_codes_data.sort_values(SEC.market_val)
    return set(sorted_tradable_codes_data.head(5)['code'].values)

def adjust_position(stock_set):
    for stock in stock_set:
        order_target_percent(stock, 1.0/len(stock_set))

def handle_bar(context, bars):
    # get feasible codes
    current_date = config.getStrDate(bars.getDateTime())
    if not is_trading_day(bars):
        return
    LOGGER.info("-----------------------------------running day %s----------------------------" % current_date)
    get_stock_fundamental_data()
    stocks_to_buy = get_top_stocks()
    adjust_position(stocks_to_buy)
