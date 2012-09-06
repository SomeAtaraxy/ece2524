# ECE 2524 Homework 2 Problem 1 Collin Schumann
with open('/etc/passwd', 'r') as f:
    # or read it line by line
    for line in f:
        array = line.split(':')
        print array[0] + '\t' + array[6]
