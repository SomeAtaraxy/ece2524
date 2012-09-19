#!/usr/bin/env python

#Collin Schumann
#ECE 2524
#HW3 mult.py

import argparse, sys

parser = argparse.ArgumentParser(description='Process some numbers.')
args = parser.parse_args()

# Initialize the product storage variable
product = 1

while True:
    try:
        # Propmpt for an number to multiply
        number = raw_input()
    except EOFError:    # ^D specification
        print '^D'
        break   # Break out of while loop

    # Blank line specification
    if number == '':
        # Print and reset
        print product
        product = 1
    else:
        # Multiply the input number by the current product
        try:
            product *= int(number)
        except ValueError:
            print 'could not convert string to float:', number
            sys.exit(1)


print product
