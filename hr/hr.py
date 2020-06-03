""" Human resources module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * birth_year (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
from os import path

hr_path = path.dirname(__file__)
filename = path.join(hr_path, 'persons.csv')
title_list = ["ID", "Name", "Birth year"]
input_list = ["Name", "Birth year"]
person_id = 0
person_name = 1
person_year = 2


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """
    table = data_manager.get_table_from_file(filename)
    title = "Human Resources menu"
    list_options = ["Show table",
                    "Add",
                    "Remove",
                    "Update",
                    "Oldest person",
                    "Person closest to average"]
    exit_message = "Exit menu"
    while True:
        ui.print_menu(title, list_options, exit_message)
        inputs = ui.get_inputs(["Please enter a number: "], "")
        option = inputs[0]
        if option == "1":
            show_table(table)
        elif option == "2":
            add(table)
        elif option == "3":
            list_labels = ["id"]
            title = "Please provide index to be removed"
            try:
                item_id = ui.get_inputs(list_labels, title)[0]
            except NameError:
                ui.print_error_message("You typed wrong id!")
            remove(table, item_id)
        elif option == "4":
            list_labels = ["id"]
            title = "Please provide"
            try:
                item_id = str(ui.get_inputs(list_labels, title)[0])
            except NameError:
                ui.print_error_message("You typed wrong id!")
            update(table, item_id)
        elif option == "5":
            ui.print_result(get_oldest_person(table),
                            'The oldest person is/are:\n')
        elif option == "6":
            ui.print_result(get_persons_closest_to_average(
                table), 'Person closest to the average is:\n')
        elif option == "0":
            data_manager.write_table_to_file(
                path.join(hr_path, 'persons.csv'), table)
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

    new_birth = 2
    while True:
        new_record = ui.get_inputs(
            input_list, "Please provide personal information:\n")
        new_record.insert(0, common.generate_random([]))
        if not new_record[new_birth].isdigit() or not int(new_record[new_birth]) >= 1900 or not int(new_record[new_birth]) <= 2020:
            ui.print_error_message(
                "Wrong value typed. Year must be higher than 1900 and lower than 2020")
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

    edited_birth = 2
    index = common.get_ind(table, person_id, id_)
    for element in table:
        if element[person_id] == id_:
            while True:
                edited_record = ui.get_inputs(
                    input_list, "Please provide personal information:\n")
                edited_record.insert(0, id_)
                if not edited_record[edited_birth].isdigit() or not int(edited_record[edited_birth]) >= 1900 or not int(edited_record[edited_birth]) <= 2020:
                    ui.print_error_message(
                        "Wrong value typed. Year must be higher than 1900 and lower than 2020")
                else:
                    table[index] = edited_record
                    break
    return table


# special functions:
# ------------------

def get_oldest_person(table):
    """
    Question: Who is the oldest person?

    Args:
        table (list): data table to work on

    Returns:
        list: A list of strings (name or names if there are two more with the same value)
    """

    temp_list = []
    for element in table:
        temp_list.append(int(element[2]))

    min_year = min(temp_list)

    min_year_records = []

    for element in table:
        if int(element[2]) == min_year:
            min_year_records.append(element[1])

    return min_year_records


def get_persons_closest_to_average(table):
    """
    Question: Who is the closest to the average age?

    Args:
        table (list): data table to work on

    Returns:
        list: list of strings (name or names if there are two more with the same value)
    """

    temp_list = []
    for element in table:
        temp_list.append(int(element[2]))

    current = 2020
    s_years = 0
    for element in temp_list:
        s_years += (current - element)

    average = s_years/len(temp_list)
    closest = []
    i = 0
    while len(closest) == 0:
        for element in table:
            if (current - int(element[2])) == average + i or (current - int(element[2])) == average - i:
                closest.append(element[1])
        i += 0.1

    return closest
