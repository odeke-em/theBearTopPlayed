#!/usr/bin/env python3
import sys, subprocess
import time

import cruncher # Local module

SLEEP_TIMEOUT = 60 * 60 # Every hour

def main():
    while 1:
        cruncher.main()
        print('\033[47m%s::Sleeping for %d seconds. Refresh at: %s\033[00m'%(
            time.ctime(), SLEEP_TIMEOUT, time.ctime(time.time() + SLEEP_TIMEOUT)
        ))
        time.sleep(SLEEP_TIMEOUT)

if __name__ == '__main__':
    main()
