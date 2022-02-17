#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:07:36 2022

@author: alumno
"""

from multiprocessing import Process, BoundedSemaphore
from multiprocessing import Value, Array

N = 4 # cantidad total de procesos

def task(common, tid, critical, bounded):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        critical[tid] = 1
       
        bounded.acquire() # nuestro wait
        
        try:
            print(f'{tid}−{i}: Critical section')
            v = common.value + 1
            print(f'{tid}−{i}: Inside critical section')
            common.value = v
            print(f'{tid}−{i}: End of critical section')
            critical[tid] = 0
        finally:
            bounded.release() # nuestro signal

    
# 1 es la cantidad de procesos que pueden estar en la seccion critica al mismo tiempo, con 2 o mas no funciona
def main():
    bounded = BoundedSemaphore(1) 
    lp = []
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, critical, bounded)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")

if __name__ == "__main__":
    main()
