from aliquant.runner import *

def initilize(context):
    context.code = "000538.SZ"
    set_stock_pool(context.code)
    context.price = GetPrice(context.code)
    context.sma = SMA(context.code, window_size=5) # ma5

def handle_bar(context, bars):
    # buy in stocks
    if context.sma[-1] > context.price[-1]: # if price > ma5, buy stock
        order_target_percent(context.code, 0.3)

    # sell stocks
    elif BROKER.getShares(context.code) > 0 and BROKER.getCumuReturn() > 0.10:
        shares = int(BROKER.getShares(context.code)*0.9)
        if shares > 0:
            order_shares(context.code,int(-1* BROKER.getShares(context.code)*0.8))
