import aliquant.client

client = aliquant.client.DefaultClient("appId", "appSecret", "endpoint")
code = '''
from aliquant.runner import *
def run(paramdict):
    pb_min = paramdict.get("pb_min",0)
    pb_max = paramdict.get("pb_max",40)
    dateList = paramdict.get("datelist", [])
    industry = get_industry_info("000538.SZ")
    codes = get_industry_stocks(industry)
    result = {}
    for d in dateList:
        q = query(SEC.code, SEC.market_val, SEC.pb).filter(Filter(SEC.pb).between(pb_min, pb_max)).order_by(SEC.market_val, asc=False).order_by(SEC.pb, asc=False).top(10)
        data = get_fundamentals(q, start_date=d) # data is type of dataFrame
        result[d] = list(data[SEC.code])
    return result, codes
'''
### parameter dict
params = {
    "pb_min":2,
    "pb_max":30,
    "datelist":['2017-04-17','2017-04-18']
}

jobId, r = client.execute(code, params)

print 'result:'
print r[0]
print r[1]