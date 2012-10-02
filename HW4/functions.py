from sys import stderr,exit

# Return a list to be appended to the main list
# Note: Field and value pairs can be in any order
def add_record(linein):
    # Initialize a temp list, so fields can be placed in
    # the correct fields
    temp = [None, None, None, 0]

    # Convert the messy split command list into a clean list
    linein = [item.strip("{}'\":,") for item in linein]

    linein.pop(0) # Remove add command

    # Place new info into appropriate field
    while len(linein) != 0:
        field = linein.pop(0)
        if field == "Quantity":
            temp[enum(field)] = int(linein.pop(0))
        else:
            temp[enum(field)] = linein.pop(0)

    return temp # Return data to be appended

# Remove a part from list and return the list
def remove_record(data, linein):
    temp =[]

    linein.pop(0) # Remove 'remove' command

     # Merge the rest

    # Split field and value
    field, val = ' '.join(linein).split('=')

    # Strip single quotes for use with description
    val = val.strip("'")

    # Remove part
    for item in data:
        if field == "Quantity":
            if int(val) != item[enum(field)]:
                temp.append(item)
        else:
            if val != item[enum(field)]:
                temp.append(item)

    # Check if the list is changed
    if len(data) != len(temp):
        return temp
    else:
        stderr.write("Invalid field-value pair for remove function: " + \
                     field + ": " + val + "\n")
        exit(2)

# Set specific values in the data list and return the list
def set_record(data, linein):
    # Parse the required variables
    setField, setVal = linein[1].split('=')
    matchField, matchVal = linein[3].split('=')

    # Iterate through all parts
    for item in data:
        # Set appropriate part(s)
        if matchVal == item[enum(matchField)]:
            if setField == "Quantity":
                item[enum(setField)] = int(setVal)
            else:
                item[enum(setField)] = setVal

    return data

# Print out entire list or list that matches a value
def list_record(data, linein):
    print 'DATA'
    print 'PartID'.ljust(8), 'Description'.ljust(34), \
          'Footprint'.ljust(12), 'Quantity'

    # Print matched value
    if len(linein) > 2:
        field, val = linein.pop(-1).split('=')
        # Compair every part to the parameter
        for item in data:
            if field == 'Quantity':
                if int(val) == item[enum(field)]:
                    print item[0].ljust(8), item[1].ljust(34), \
                        item[2].ljust(12), item[3]
            else:
                if val == item[enum(field)]:
                    print item[0].ljust(8), item[1].ljust(34), \
                        item[2].ljust(12), item[3]

    # Print entire list
    else:
        for item in data:
            print item[0].ljust(8), item[1].ljust(34), \
                  item[2].ljust(12), item[3]

    print "."
    return

# Sort the list with given field
def sort_record(data, linein):
    field = linein.pop(-1)

    # Remove ('sort', 'by') from linein
    linein.pop(-1)
    linein.pop(-1)

    # sort
    data.sort(key=lambda x: x[enum(field)])

    return data, linein

# Enumerate fields based on list index
def enum(field):
    if field == "PartID":
        return 0
    elif field == "Description":
        return 1
    elif field == "Footprint":
        return 2
    elif field == "Quantity":
        return 3
    else:
        stderr.write("Invalid field: " + field + "\n")
        exit(2)
