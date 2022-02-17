#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 10:08:58 2022

@author: alumno
"""

from multiprocessing import Process, Lock
from multiprocessing import Value, Array

N = 4 # cantidad total de procesos

def task(common, tid, critical, lock):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        critical[tid] = 1
       
        lock.acquire() # nuestro wait
        
        try:
            print(f'{tid}−{i}: Critical section')
            v = common.value + 1
            print(f'{tid}−{i}: Inside critical section')
            common.value = v
            print(f'{tid}−{i}: End of critical section')
            critical[tid] = 0
        finally:
            lock.release() # nuestro signal

    

def main():
    lock = Lock()
    lp = []
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, critical, lock)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")

if __name__ == "__main__":
    main()

