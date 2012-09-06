# ECE 2524 Homework 2 Problem 2 Collin Schumann

import sys
with open(sys.argv[1], 'r') as f:
    print "ACCOUNT INFORMATION FOR BLACKSBURG RESIDENTS"
    # or read it line by line
    for line in f:
        array = line.split()
        if array[3] == "Blacksburg":
            data = (array[4], array[0], array[1], array[2])
            print ", ".join(data)
