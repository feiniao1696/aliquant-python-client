import aliquant.client

client = aliquant.client.DefaultClient("appId", "appSecret", "endpoint")

client.uploadData('samples/data', 'data10')

code = '''
from aliquant.runner import *
def run(paramdict):
    dateList = paramdict.get("datelist", [])
    result = {}
    for d in dateList:
        q = query("code","total_a").filter(Filter("total_a").less(300000000)).filter(Filter("date").equal(d)).order_by("total_a").top(10)
        result[d]= list(q.load_data("data10")['code'])
    return result
'''
### parameter dict
params = {
 "datelist": ['2017-04-18', '2017-04-19']
}

jobId, r = client.execute(code, params)

print 'result:'
print r
