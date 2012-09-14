"""
Implementation of sleep sort.
"""

import random
import time
import threading
import collections


TURBO = 100.0


class Sleeper(threading.Thread):
    def __init__(self, func, sleep_time):
        threading.Thread.__init__(self)
        self.func = func
        self.sleep_time = sleep_time

    def run(self):
        """Sleeps x time and calls func with
        sleep_time as a parameter.
        """
        # Sleeping less makes this faster, but also
        # more error prone
        time.sleep(self.sleep_time / TURBO)
        self.func(self.sleep_time)


def sleep_sort(l):
    deque = collections.deque()
    threads = []
    for i in l:
        thread = Sleeper(deque.append, i)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return [x for x in deque]


def main():
    print('testing sort..')
    iterations = 5
    list_length = 30

    for x in range(iterations):
        l = [random.randint(1, 10) for x in xrange(list_length)]
        sleep_sorted = sleep_sort(l)
        if sleep_sorted != sorted(l):
            print('sleep sort did not sort correctly this time.')
            print('original:\t\t%s' % l)
            print('sleep sorted:\t%s' % sleep_sorted)
            print('sorted:\t\t\t%s\n' % sorted(l))


if __name__ == '__main__':
    main()

