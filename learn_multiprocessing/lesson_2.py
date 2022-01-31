"""
Basic multiprocessing
"""

import multiprocessing
import time


def do_something(seconds):
    print(f'Sleeping {seconds} sec(s)...')
    time.sleep(seconds)
    print(f'Done sleeping for {seconds} sec(s)...')


if __name__ == '__main__':

    start = time.perf_counter()

    # p1 = multiprocessing.Process(target=do_something)
    # p2 = multiprocessing.Process(target=do_something)
    #
    # p1.start()
    # p2.start()
    #
    # p1.join()
    # p2.join()

    processes = []
    for _ in range(10):
        # multiprocessing.freeze_support()
        p = multiprocessing.Process(target=do_something, args=[1.5])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f'Time elapsed: {finish - start:.5f} secs')
