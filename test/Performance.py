import threading
import requests
import time


def worker(num,api):
    """thread worker function"""
    print ("Request Number %s " % (num))
    response = requests.get(api)
    return

#Test x calls in x intervals
def xPerMin(interval,calls,api,name):
    fh = open("Performance.txt", "a")
    threads = []
    now = time.time()
    currInterval = 0
    for i in range(calls):
        t = threading.Timer(currInterval,worker,[i,api])
        currInterval += interval
        threads.append(t)
        t.start()
    for x in threads:
        x.join()
    fh.write("%s : Total time for %s requests to finish is %s seconds, at rate : %s \n" % (name, calls, time.time() - now,interval))
    fh.close()

#do x calls as quick as possible
def xCalls(calls,api,name):
    threads = []
    now = time.time()
    fh = open("Performance.txt", "a")
    for i in range(calls):
        t = threading.Thread(target=worker, args=(i,api))
        threads.append(t)
        t.start()
    for x in threads:
        x.join()
    fh.write("%s : Total time for %s requests to finish is %s seconds\n" % (name,calls,time.time()-now))
    fh.close()

def main():
    fh = open("Performance.txt", "a")
    apis = {}
    #get the apis from the text
    with open('perfInputs.txt', 'r') as f:
        for line in f:
            words = line.split()
            apis[words[0]] = words[1]


    '''
    for key in apis:
        print("Testing 1 call on api: " + key)
        xCalls(1,apis[key],key)
        print("Testing 10 calls on api: " + key)
        xCalls(10, apis[key], key)
        print("Testing 100 calls on api: " + key)
        xCalls(100, apis[key], key)
        print("Testing 300 calls on api: " + key)
        xCalls(300, apis[key], key)
     '''
    for key in apis:
        print("Testing 1 call on api: " + key)
        xPerMin(1,1,apis[key],key)
        print("Testing 10 calls on api: " + key)
        xPerMin(1/10, 10, apis[key], key)
        print("Testing 100 calls on api: " + key)
        xPerMin(1/100, 100, apis[key], key)
        print("Testing 3400 calls on api: " + key)
        xPerMin(1/300, 300, apis[key], key)

    fh.close()
if __name__ == "__main__":
    main()