""" Common module
implement commonly used functions here
"""

import random


def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation:
         - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letter
         - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """

    # Your code

    id_gen_list = []
    generated = ''

    id_gen_list.append(chr(random.randrange(97, 122)))  # Lower case char
    id_gen_list.append(chr(random.randrange(65, 90)))  # Upper case char
    id_gen_list.append(chr(random.randrange(48, 57)))  # Number
    id_gen_list.append(chr(random.randrange(48, 57)))
    id_gen_list.append(chr(random.randrange(65, 90)))
    id_gen_list.append(chr(random.randrange(97, 122)))
    id_gen_list.append(chr(random.randrange(33, 47)))  # Special char
    id_gen_list.append(chr(random.randrange(33, 47)))

    for element in id_gen_list:
        generated += element

    return generated


def get_ind(table, column, data):
    """
    Finds index of item by provided data

    Args:
        table (list): Data table to work on. First columns containing the keys.
        column(int): Column to iterate for.
        data(str): Data to look for.

    Returns:
        int: Index of data in speciefied column.
    """
    index = -1
    for element in table:
        index += 1
        if element[column] == data:
            return index


def quicksrt(array):
    """
    Quicksort algorithm implementation for sorting strings.

    Args:
        array (list): List to sort.

    Returns:
        list: Sorted list of strings.
    """

    lst = []

    for element in array:
        temp = []
        for i in element:
            temp.append(ord(i))
        lst.append(temp)

    length = len(lst)
    if length <= 1:
        return array
    else:
        pivot = lst.pop()

    items_greater = []
    items_lower = []

    for item in lst:
        i = 0
        while item[i] == pivot[i]:
            i += 1
        if item[i] < pivot[i]:
            temp_item = ""
            for element in item:
                temp_element = chr(int(element))
                temp_item += temp_element
            items_lower.append(temp_item)
        elif item[i] > pivot[i]:
            temp_item = ""
            for element in item:
                temp_element = chr(int(element))
                temp_item += temp_element
            items_greater.append(temp_item)

    piv_str = ""
    for i in pivot:
        temp_element = chr(int(i))
        piv_str += temp_element

    return quicksrt(items_lower) + [piv_str] + quicksrt(items_greater)
