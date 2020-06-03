""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
"""
# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
from os import path

acc_path = path.dirname(__file__)
table = []
table = data_manager.get_table_from_file(path.join(acc_path, 'items.csv'))
print


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    title = "Accounting menu"
    list_options = ["Show table",
                    "Add",
                    "Remove",
                    "Update",
                    "Max year",
                    "Averege profit in year"]
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
            which_year_max(table)
        elif option == "6":
            list_labels = ["Year"]
            title = "Please provide"
            year = ui.get_inputs(list_labels, title)[0]
            avg_amount(table, int(year))
        elif option == "0":
            data_manager.write_table_to_file(
                path.join(acc_path, 'items.csv'), table)
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

    title_list = ["ID", "Month", "Day", "Year", "Type", "Amount"]
    ui.print_table(table, title_list)


def is_correct(record):
    month = 1
    day = 2
    year = 3
    type = 4
    amount = 5

    if not record[month].isdigit() or not int(record[month]) >= 1 or not int(record[month]) <= 12:
        ui.print_error_message("Wrong value typed. Months can be 1 -> 12")
    elif not record[day].isdigit() or not int(record[day]) >= 1 or not int(record[day]) <= 31:
        ui.print_error_message("Wrong value typed. Days can be 1 -> 31")
    elif not record[year].isdigit() or not int(record[year]) >= 1990 or not int(record[day <= 2020]):
        ui.print_error_message(
            "Wrong value typed. Year must be higher than 1990 and lower than 2020")
    elif not record[type] == 'in' and not record[type] == 'out':
        # if not record[type] == 'out':
        ui.print_error_message("Type must be 'in' or 'out'")
    elif not record[amount].isdigit() or not int(record[amount]) >= 0:
        ui.print_error_message("Amount must be positive value")
    else:
        return True


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    list_labels = ["month", "day", "year", "type", "amount"]
    title = "Please provide"
    new_record = []
    while True:
        new_record = ui.get_inputs(list_labels, title)
        new_record.insert(0, common.generate_random(table))
        if is_correct(new_record):
            break
    # We need to convert inputs to right types and check if they have sense
    table.append(new_record)
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

    person_id = 0
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

    list_labels = ["month", "day", "year", "type", "amount"]
    title = "Please provide"
    person_id = 0
    new_data = []
    myindex = common.get_ind(table, person_id, id_)
    for element in table:
        if element[person_id] == id_:
            while True:
                new_data = ui.get_inputs(list_labels, title)
                new_data.insert(0, id_)
                if is_correct(new_data):
                    break
    table[myindex] = new_data
    return table


# special functions:
# ------------------
def profit(table):
    dict = {}
    year = 3
    is_income = 4
    amount = 5
    for row in table:
        dict[row[year]] = 0
    for row in table:
        if row[is_income] == 'in':
            dict[row[year]] += int(row[amount])
        if row[is_income] == 'out':
            dict[row[year]] -= int(row[amount])
    return dict


def which_year_max(table):
    """
    Question: Which year has the highest profit? (profit = in - out)

    Args:
        table (list): data table to work on

    Returns:
        number
    """

    max_value = 0
    which_year = 0
    mydict = profit(table)
    for e in mydict:
        if mydict[e] > max_value:
            max_value = mydict[e]
    for element in mydict:
        if mydict[element] == max_value:
            which_year = int(element)
    label = 'Year with highest profit is: '
    ui.print_result(which_year, label)
    return which_year


def avg_amount(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]

    Args:
        table (list): data table to work on
        year (number)

    Returns:
        number
    """

    sum_amount = 0
    count_amount = 0
    for element in table:
        if int(element[3]) == year:
            if element[4] == "in":
                sum_amount += int(element[5])
                count_amount += 1
            elif element[4] == "out":
                sum_amount -= int(element[5])
                count_amount += 1

    return (sum_amount/count_amount)
