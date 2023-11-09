#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 09:56:26 2023

@author: spet5177
"""
# This gives the unit cell length of a C-C or B-N tube based on the n,m values. 
# When making MWNT I will need to scan through length values for different
# n,m for C-C and B-N to find tubes that will allign (lowest common multiple)
# so that they can both fit in the periodic box for simulation



import sys
import numpy as np

n = int(sys.argv[1])
m = int(sys.argv[2])


def hcf_calc(x,y):
    if x == 0:
        hcf = y
    elif y == 0:
        hcf = x
    elif x >y: 
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller+1):
        if ((x % i == 0) and (y % i == 0)):
            hcf = i
    return hcf

hcf = hcf_calc(n,m)

def length_calc(n,m):
    if sys.argv[3] == None:
        print("Enter command line arguement of C or BN")
    elif sys.argv[3] == "C":
        r = 1.418 / 0.529177
        length = (3 * r * np.sqrt((n**2 + m**2 + n*m))) / hcf
    elif sys.argv[3] == "BN":
        r = 1.446
        length = (3 * r * np.sqrt((n**2 + m**2 + n*m))) / hcf
    else:
        pass
    return length

print("The legnth of the tube in A is: ", length_calc(n, m))


