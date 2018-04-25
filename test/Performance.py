import threading
import requests
import time


def worker(num):
    """thread worker function"""
    print ("Request Number %s " % (num))
    reponse = requests.get("http://seng3011laser.com/api/v2/PageData?company=woolworths&startdate=2015-10-01T08%3A45%3A10.295Z&enddate=2015-11-02T19%3A37%3A12.193Z&fields=id%2Cname%2Cfan_count%2Cwebsite%2Cposts.fields(post_comment_count%2Cpost_type%2Cpost_message%2Cpost_created_time)")
    return

#Test x calls in x intervals
def xPerMin(interval,calls):
    fh = open("Performance.txt", "a")
    threads = []
    now = time.time()
    currInterval = 0
    for i in range(calls):
        t = threading.Timer(currInterval,worker,[i])
        currInterval += interval
        threads.append(t)
        t.start()
    for x in threads:
        x.join()
    fh.write("Total time for requests to finish is time is %s\n" % (time.time()-now))
    fh.close()

#do x calls as quick as possible
def xCalls(calls):
    threads = []
    now = time.time()
    fh = open("Performance.txt", "a")
    for i in range(calls):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    for x in threads:
        x.join()
    fh.write("Total time for requests to finish is time is %s\n" % (time.time()-now))
    fh.close()

def main():
    xPerMin(1,1)
    xPerMin(1,1)

if __name__ == "__main__":
    main()