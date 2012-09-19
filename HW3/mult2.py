#!/usr/bin/env python

#Collin Schumann
#ECE 2524
#HW3 mult2.py

import argparse, sys

parser = argparse.ArgumentParser(description='Process some numbers.')
parser.add_argument('infile', type=argparse.FileType('r'), nargs='?',
                   default=sys.stdin, help='a file to have multiplied')
parser.add_argument('--ignore-blank', action='store_true',
                   help='Ignore blank lines')
parser.add_argument('--ignore-non-numeric', action='store_true',
                   help='Ignore non-numeric lines')
args = parser.parse_args()

# Initialize the product storage variable
product = 1

# I couln't figure out how to combine these, so I seperated them
# If input is the terminal
if args.infile == sys.stdin:
    while True:
        try:
            # Propmpt for an number to multiply
            number = raw_input()
        except EOFError:    # ^D specification
            print '^D'
            break   # Break out of while loop

        # Blank line specification
        if number == '':
           if not(args.ignore_blank):
                # Print and reset
                print product
                product = 1
        else:
            # Multiply the input number by the current product
            try:
                product *= int(number)
            except ValueError:
                if not(args.ignore_non_numeric):
                    print 'could not convert string to float:', number
                    sys.exit(1)
# If input is a file
else:
    for line in args.infile:
        # Blank line specification
        if line == '\n':
           if not(args.ignore_blank):
                # Print and reset
                print product
                product = 1
        else:
            # Multiply the input number by the current product
            try:
                product *= int(line)
            except ValueError:
                if not(args.ignore_non_numeric):
                    print 'could not convert string to float:', line
                    sys.exit(1)

print product
