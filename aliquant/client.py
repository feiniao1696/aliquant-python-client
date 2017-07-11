import sys
import time
import oss2
import json
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant

try:
  import cPickle as pickle
except:
  import pickle as  pickle


class DefaultClient:
  def __init__(self, app_key=None, app_secret=None, app_host=None, app_endpoint="https://oss-cn-shanghai.aliyuncs.com", app_bucket="aliquant", time_out=None):
    self.__app_key = app_key
    self.__app_secret = app_secret
    self.__time_out = time_out
    self.__host = app_host
    self.__endpoint = app_endpoint
    self.__bucket = app_bucket
    self.cli = client.DefaultClient(app_key=app_key, app_secret=app_secret, time_out=time_out)
    pass

  def execute(self, code, params):
    print "creating job"
    req_post = request.Request(host=self.__host, protocol=constant.HTTP, url="/job", method="POST", time_out=30000)
    req_post.set_body(bytearray(source=json.dumps({"code": code, "params": pickle.dumps(params)}), encoding="utf8"))
    req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
    a, b, res = self.cli.execute(req_post)

    # debug
    print res

    try:
      r = json.loads(res)
    except:
      print a, b, res
      return

    if r['success'] != True:
      print r
      return

    print 'jobId is ' + r['jobId']

    token = r['credential']
    auth = oss2.StsAuth(token['AccessKeyId'], token['AccessKeySecret'], token['SecurityToken'])
    bucket = oss2.Bucket(auth, self.__endpoint, self.__bucket)

    nextLogPosition = 0

    while 1:
      req = request.Request(host=self.__host, protocol=constant.HTTP, url='/result/' + r['jobId'], method="GET",
                            time_out=3000)
      a, b, rr = self.cli.execute(req)

      try:
        jsonObj = json.loads(rr)
      except:
        print 'get result error:', a, b, rr
        continue

      if jsonObj['success'] != True:
        print jsonObj
        return

      print jsonObj['status']

      try:
        log_desc = bucket.head_object(r['logPath'])
        l = log_desc.content_length - 1

        if l > nextLogPosition:
          log_stream = bucket.get_object(r['logPath'], byte_range=(nextLogPosition, l))
          log = log_stream.read()
          sys.stdout.write(log)
          sys.stdout.flush()
          with open('logs/job' + r['jobId'] + '.log', 'a') as the_file:
            the_file.write(log)
          nextLogPosition = l
      except:
        pass

      if jsonObj['status'] == 'finished':
        try:
          result_desc = bucket.head_object(r['resultPath'])
          print 'result length is ' + str(result_desc.content_length)
          result_stream = bucket.get_object(r['resultPath'])
          return pickle.loads(result_stream.read())
        except:
          raise
          pass

      time.sleep(1)

  def uploadData(self, localPath, uploadName):
    print 'uploading data'
    req = request.Request(host=self.__host, protocol=constant.HTTP, url='/credential/upload/data/' + uploadName, method="GET",
                          time_out=3000)
    a, b, rr = self.cli.execute(req)

    try:
      res = json.loads(rr)
    except:
      print a, b, rr
      return

    if res['success'] != True:
      print res
      return

    token = res['credential']

    auth = oss2.StsAuth(token['AccessKeyId'], token['AccessKeySecret'], token['SecurityToken'])

    bucket = oss2.Bucket(auth, self.__endpoint, self.__bucket)

    oss2.resumable_upload(bucket, res['path'], localPath)

    print 'upload complete'
