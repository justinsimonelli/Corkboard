__author__ = 'jxs699'
import json, dbUtil

def runDbUtil():
    data = [dict(message="dbTest class test 2", latitude="198", longitude="247")]
    status = dbUtil.insert_new_msg(data)
    print("status:" + status['status'] )


if __name__ == "__main__":
    #runDbScript()
    runDbUtil()