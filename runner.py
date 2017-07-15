import sys
import os
import aliquant.client
import aliquant.config

# TODO
client = aliquant.client.DefaultClient(aliquant.config.appId, aliquant.config.appSecret, aliquant.config.endpoint)
client = aliquant.client.DefaultClient(aliquant.config.appId, aliquant.config.appSecret, aliquant.config.endpoint, app_bucket = aliquant.config.app_bucket)

params = {
  'start_date': '2011-01-01',
  'end_date': '2017-01-01',
  'init_cash': 1000000,
  "bar_type":"d"
}

def main():
    if len(sys.argv) < 2:
        print "[ERROR] Not enough input, usage: python runner.py code_file.py" 
        return

    code_file = sys.argv[1]
    if not os.path.exists(code_file):
        print "[ERROR] code_file [%s] does not exsist" % code_file
    code = open(code_file).read()

    jobId, r = client.execute(code, params)
    print 'result:'
    print r
    client.plot('logs/job' + jobId + '.log') 
    return jobId, r

if __name__ == "__main__":
    main()
