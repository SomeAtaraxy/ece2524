# ECE 2524 Homework 2 Problem 3 Collin Schumann

import sys
total = 0.0
people = 0
maxnum = float("-inf")
minnum = float("inf")
with open(sys.argv[1], 'r') as f:
    # or read it line by line
    for line in f:
        array = line.split()
        people += 1
        total += float(array[2])
        if float(array[2]) > maxnum:
            maxnum = float(array[2])
            maxname = array[1]
        if float(array[2]) < minnum:
            minnum = float(array[2])
            minname = array[1]

print "ACCOUNT SUMMARY"
print "Total amount owed =", '{:0.2f}'.format(total)
print "Average amount owed =", '{:0.2f}'.format(round(total/people, 1))
print "Maximum amount owed =", '{:0.2f}'.format(maxnum), "by", maxname
print "Minimum amount owed =", '{:0.2f}'.format(minnum), "by", minname
