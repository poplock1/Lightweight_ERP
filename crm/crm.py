""" Customer Relationship Management (CRM) module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * email (string)
    * subscribed (int): Is she/he subscribed to the newsletter? 1/0 = yes/no
"""

# User interface module
import ui
# data manager module
import data_manager
# common module
import common
from os import path

crm_path = path.dirname(__file__)
title_list = ["ID", "Name", "Email", "Subscribed to newsletter (1/0 = yes/no)"]
input_list = ["Name", "Email", "Subscribed to newsletter (1/0 = yes/no)"]
filename = path.join(crm_path, 'customers.csv')
person_id = 0
person_name = 1
person_email = 2
person_subscribed = 3


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file(filename)
    options = ["Show table",
               "Add",
               "Remove",
               "Update",
               "Get longest name",
               "Subscribers"]
    while True:
        ui.print_menu("Customer Relationship Menagement menu",
                      options, "Exit menu")
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]
        if option == "1":
            show_table(table)
        elif option == "2":
            table = add(table)
        elif option == "3":
            show_table(table)
            id_is_correct = 0
            while id_is_correct == 0:
                id_ = ui.get_inputs(["ID to remove:"],
                                    "Please select index from table above")
                id_ = ''.join(str(e) for e in id_)
                for element in table:
                    if id_ == element[person_id]:
                        table = remove(table, id_)
                        id_is_correct += 1
                if id_is_correct == 0:
                    ui.print_error_message("ID not in list")
        elif option == "4":
            show_table(table)
            id_is_correct = 0
            while id_is_correct == 0:
                id_ = ui.get_inputs(["ID to update:"],
                                    "Please select index from table above")
                id_ = ''.join(str(e) for e in id_)
                for element in table:
                    if id_ == element[person_id]:
                        table = update(table, id_)
                        id_is_correct += 1
                if id_is_correct == 0:
                    ui.print_error_message("ID not in list")
        elif option == "5":
            ui.print_result(get_longest_name_id(table), "Longest name:\n")
        elif option == "6":
            ui.print_result(get_subscribed_emails(table), "Subscribers:\n")
        elif option == "0":
            data_manager.write_table_to_file(filename, table)
            return False
        else:
            raise KeyError("There is no such option.")


def show_table(table):
    """
    Display a table

    Args:
        table (list): list of lists to be displayed.

    Returns:
        None
    """

    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    new_name = 1
    new_email = 2
    new_subscribed = 3
    while True:
        new_record = ui.get_inputs(
            input_list, "Please provide personal information:\n")
        new_record.insert(0, common.generate_random([]))
        email = set(new_record[new_email])
        email_correct_char = set('@')
        correct_subscribe_number = ["0", "1"]
        if not new_record[new_name].replace(' ', '').isalpha():
            ui.print_error_message("Provide correct name")
        if not any((char in email_correct_char) for char in email):
            ui.print_error_message("Provide correct email adress")
        elif new_record[new_subscribed] not in correct_subscribe_number:
            ui.print_error_message("Provide correct subscribe data (1 or 0)")
        else:
            break
    table = table + [new_record]
    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """

    for element in table:
        if element[person_id] == id_:
            table.remove(element)
    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    edited_name = 1
    edited_email = 2
    edited_subscribed = 3
    index = common.get_ind(table, person_id, id_)
    for element in table:
        if element[person_id] == id_:
            while True:
                edited_record = ui.get_inputs(
                    input_list, "Please provide personal information:\n")
                edited_record.insert(0, common.generate_random([]))
                email = set(edited_record[edited_email])
                email_correct_char = set('@')
                correct_subscribe_number = ["0", "1"]
                if not edited_record[edited_name].replace(' ', '').isalpha():
                    ui.print_error_message("Provide correct name")
                if not any((char in email_correct_char) for char in email):
                    ui.print_error_message("Provide correct email adress")
                elif edited_record[edited_subscribed] not in correct_subscribe_number:
                    ui.print_error_message(
                        "Provide correct subscribe data (1 or 0)")
                else:
                    table[index] = edited_record
                    break
    return table


# special functions:
# ------------------

def get_longest_name_id(table):
    """
        Question: What is the id of the customer with the longest name?

        Args:
            table (list): data table to work on

        Returns:
            string: id of the longest name (if there are more than one, return
                the last by alphabetical order of the names)
        """
    q_list = []
    for element in table:
        q_list.append(element[1])
    alphabetical_list = common.quicksrt(q_list)
    longest_name_list = []
    length_of_name = 0
    for element in alphabetical_list:
        if len(element) >= length_of_name:
            length_of_name = len(element)
            longest_name_list.append(element)
    for names in longest_name_list:
        for element in table:
            if element[1] == names:
                return element[0]


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """
        Question: Which customers has subscribed to the newsletter?

        Args:
            table (list): data table to work on

        Returns:
            list: list of strings (where a string is like "email;name")
        """

    # your code
    subscribers = []
    for element in table:
        if int(element[person_subscribed]) == 1:
            subscribers.append(
                f'{element[person_email]}{";"}{element[person_name]}')
    return subscribers
