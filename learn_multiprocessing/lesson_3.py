"""
Demonstration of multiprocessing code
1. ALTERNATIVE 1: result is obtained as the tasks are completed. Tasks are taken based on thread availability (random).
2. ALTERNATIVE 2: task are completed as given in input sequence. Operations are ordered.
"""
import concurrent.futures
import time


def do_something(seconds):
    print(f'Sleeping {seconds} sec(s)...')
    time.sleep(seconds)
    return f'Done sleeping for {seconds} sec(s)...'


if __name__ == '__main__':

    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1]
        # ALTERNATIVE #1
        # results = [executor.submit(do_something, sec) for sec in secs]
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())

        # ALTERNATIVE #2
        op_list = []
        results = executor.map(do_something, secs)
        for result in results:
            op_list.append(result)

    print(op_list)
    finish = time.perf_counter()
    print(f'Time elapsed: {finish - start:.5f} secs')
