import aliquant.client

# client = aliquant.client.DefaultClient("24525088", "3e7af6afb851ba26b168518fae347b71", "http://aliquant.open5.net")
client = aliquant.client.DefaultClient("24525088", "3e7af6afb851ba26b168518fae347b71", "http://test.open5.net", app_bucket="aliquant-test")

code = '''
from aliquant.runner import *
def initilize(context):
    context.code = "000538.SZ"
    set_stock_pool("000538.SZ")
    context.price = GetPrice(context.code)
    context.sma = SMA(context.code, window_size=5) # ma5

def handle_bar(context, bars):

    if context.sma[-1] > context.price[-1]: # if price > ma5, buy stock
        num =int((0.3* BROKER.getCash())/bars[context.code].getClose())
        if (num > 1):
            order_shares(context.code, num)
    elif BROKER.getShares(context.code) > 0 and BROKER.getCumuReturn() > 0.10:
        shares = int(BROKER.getShares(context.code)*0.9)
        if shares > 0:
            order_shares(context.code,int(-1* BROKER.getShares(context.code)*0.8))
'''

params = {
  'start_date': '2011-01-01',
  'end_date': '2017-01-01',
  'init_cash': 1000000,
  "bar_type":"d"
}

jobId, r = client.execute(code, params)

print 'result:'
print r

client.plot('logs/job' + jobId + '.log')
