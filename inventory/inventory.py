""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
from os import path

inv_path = path.dirname(__file__)
filename = path.join(inv_path, 'inventory.csv')
title_list = ["ID", "Name", "Manufacturer", "Purchase year", "Durability"]
input_list = ["Name", "Manufacturer", "Purchase year", "Durability"]
inv_id = 0
inv_name = 1
inv_manufacturer = 2
inv_purchase = 3
inv_durability = 4


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file(filename)
    title = "Inventory menu"
    list_options = ["Show table",
                    "Add",
                    "Remove",
                    "Update",
                    "Get avilable items until given year",
                    "Get average durability by manufacturer"]
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
            ui.print_result(get_available_items(table, 2016),
                            'List of avilable items:\n')
        elif option == "6":
            ui.print_result(get_average_durability_by_manufacturers(
                table), 'Average by manufacturer is:\n')
        elif option == "0":
            data_manager.write_table_to_file(
                path.join(inv_path, 'persons.csv'), table)
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

    new_year = 3
    new_durability = 4
    while True:
        new_record = ui.get_inputs(
            input_list, "Please provide personal information:\n")
        new_record.insert(0, common.generate_random([]))
        if not new_record[new_year].isdigit() or not int(new_record[new_year]) >= 1900 or not int(new_record[new_year]) <= 2021:
            ui.print_error_message(
                "Wrong value typed. Year must be higher than 1900 and lower than 2021")
        if not new_record[new_durability].isdigit() or not int(new_record[new_durability]) >= 1 or not int(new_record[new_durability]) <= 20:
            ui.print_error_message(
                "Wrong value typed. Durability must be higher than 0 and lower than 20")
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
        if element[inv_id] == id_:
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

    new_year = 3
    new_durability = 4
    index = common.get_ind(table, inv_id, id_)
    for element in table:
        if element[inv_id] == id_:
            while True:
                new_record = ui.get_inputs(
                    input_list, "Please provide information:\n")
                new_record.insert(0, common.generate_random([]))
                if not new_record[new_year].isdigit() or not int(new_record[new_year]) >= 1900 or not int(new_record[new_year]) <= 2021:
                    ui.print_error_message(
                        "Wrong value typed. Year must be higher than 1900 and lower than 2021")
                if not new_record[new_durability].isdigit() or not int(new_record[new_durability]) >= 1 or not int(new_record[new_durability]) <= 20:
                    ui.print_error_message(
                        "Wrong value typed. Durability must be higher than 0 and lower than 20")
                else:
                    table[index] = new_record
                    break
    return table


# special functions:
# ------------------

def get_available_items(table, year):
    """
    Question: Which items have not exceeded their durability yet (in a given year)?

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """

    avilable = []
    current = year
    for element in table:
        if (current - int(element[3])) < int(element[4]):
            avilable.append(element)
    for element in avilable:
        element[3] = int(element[3])
        element[4] = int(element[4])

    return avilable


def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """

    average_dict = {}
    for element in table:
        if element[2] not in average_dict:
            average_dict[element[2]] = 0
    for key in average_dict:
        sum_years = 0
        count_manufacterers = 0
        for element in table:
            if element[2] == key:
                sum_years += int(element[4])
                count_manufacterers += 1
        average_dict[key] = sum_years/count_manufacterers

    return average_dict
