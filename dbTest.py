__author__ = 'jxs699'
import json, dbUtil, app, jsonpickle

def runDBUtilPost():
    data = [dict(message="dbTest class test 2", latitude="198", longitude="247")]
    status = dbUtil.insert_new_msg(data)
    print("status:" + status['status'] )

def runDBUtilGetLatest():
    result = dbUtil.get_latest_record()
    record = result['item'][0]
    serialized = record.test()

    #print("latest record: " + str(record.serialize()))

if __name__ == "__main__":
    #runDbScript()
    #runDBUtilPost()
    runDBUtilGetLatest()