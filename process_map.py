"""
Multiprocessing map testing
"""

import multiprocessing
import time

def process_map(func, iterable):
    # By default, pool will use as many separate processes as there are CPU
    # cores. See multiprocessing.cpu_count()
    pool = multiprocessing.Pool()

    # multiprocessing module's documentation uses term result object, here
    # task is used instead.
    tasks = []

    for item in iterable:
        tasks.append(pool.apply_async(func, [item]))

    # Wait until tasks are complete to get results
    results = [task.get(timeout=None) for task in tasks]

    return results


def main():
    print('Started..')
    process_map(time.sleep, [1, 2, 1, 2, 1, 2, 1, 2, 1])
    print('Finished')



if __name__ == '__main__':
    main()
