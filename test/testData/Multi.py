import asyncio
import concurrent.futures
import requests
import time

async def main(num_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as num_workers: # set up 20 threads
        loop = asyncio.get_event_loop()
        make_requests = [
            loop.run_in_executor(
                num_workers,
                requests.get,
                'http://seng3011laser.com/api/v2/PageData?company=woolworths&startdate=2015-10-01T08%3A45%3A10.295Z&enddate=2015-11-02T19%3A37%3A12.193Z&fields=id,name,fan_count,website,posts.fields(post_comment_count,post_type,post_message,post_created_time)'
            )
            for i in range(num_requests)
        ]

def test():
    requests = [20,50,100,500,1000,2000]
    file = open("Multi.txt", "a")
    for i in requests:
        loop = asyncio.get_event_loop() # basically prepping one of the threads to loop
        start = time.time()
        loop.run_until_complete(main(i)) # loop until it's done
        end = time.time()
        file.write("Total time to make %i requests is %s seconds \n" % (i, (end-start)))

    file.close()

if __name__ == "__main__":
    test()



