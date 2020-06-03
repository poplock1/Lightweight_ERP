""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
from os import path

store_path = path.dirname(__file__)
filename = path.join(store_path, 'games.csv')
title_list = ["ID", "Game title", "Manufacturer", "Price in USD", "Count"]
input_list = ["Game title", "Manufacturer", "Price in USD", "Count"]
game_id = 0
game_title = 1
game_manufacturer = 2
game_price = 3
game_count = 4


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file(filename)
    while True:
        options = ["Show table",
                   "Add",
                   "Remove",
                   "Update",
                   "Count games by manufacturer",
                   "Average amount of games by manufacturer"]
        ui.print_menu("Store Menagement menu", options, "Exit menu")
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
                id_ = ui.get_inputs(["Index to remove:"],
                                    "Please select index from table above")
                id_ = ''.join(str(e) for e in id_)
                for games in table:
                    if games[game_id] == id_:
                        table = remove(table, id_)
                        id_is_correct += 1
                if id_is_correct == 0:
                    ui.print_error_message("ID not in list")
        elif option == "4":
            show_table(table)
            id_is_correct = 0
            while id_is_correct == 0:
                id_ = ui.get_inputs(["Index to remove:"],
                                    "Please select index from table above")
                id_ = ''.join(str(e) for e in id_)
                for games in table:
                    if games[game_id] == id_:
                        table = update(table, id_)
                        id_is_correct += 1
                if id_is_correct == 0:
                    ui.print_error_message("ID not in list")
        elif option == "5":
            ui.print_result(get_counts_by_manufacturers(table), "Label")
        elif option == "6":
            correct_input = 0
            while correct_input == 0:
                manufacturers_list = []
                for games in table:
                    if games[game_manufacturer] not in manufacturers_list:
                        manufacturers_list.append(games[game_manufacturer])
                ui.print_result(manufacturers_list,
                                "List of manufacturers: \n")
                manufacturer = ui.get_inputs(
                    ["Manufacturer: "], "Provide data")
                manufacturer = ''.join(str(e) for e in manufacturer)
                for element in manufacturers_list:
                    if manufacturer == element:
                        ui.print_result(get_average_by_manufacturer(table, manufacturer),
                                        "Average amount of games by manufacturer:\n")
                        correct_input += 1
                if correct_input == 0:
                    ui.print_error_message("Manufacturer not in list")
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

    new_price = 3
    new_count = 4
    while True:
        new_record = ui.get_inputs(
            input_list, "Please provide personal information:\n")
        new_record.insert(0, common.generate_random([]))
        if not new_record[new_price].replace('.', '').isdigit():
            ui.print_error_message("Provide correct price")
        elif not new_record[new_count].isdigit():
            ui.print_error_message("Provide correct count")
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
        if element[game_id] == id_:
            table.remove(element)
    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """

    new_price = 3
    new_count = 4
    index = common.get_ind(table, game_id, id_)
    for element in table:
        if element[game_id] == id_:
            while True:
                new_record = ui.get_inputs(
                    input_list, "Please provide personal information:\n")
                new_record.insert(0, common.generate_random([]))
                if not new_record[new_price].replace('.', '').isdigit():
                    ui.print_error_message("Provide correct price")
                elif not new_record[new_count].isdigit():
                    ui.print_error_message("Provide correct count")
                else:
                    table[index] = new_record
                    break
    return table


# special functions:
# ------------------

def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """

    manufacturers = []
    dict_ = {}
    for games in table:
        manufacturers.append(games[game_manufacturer])
    for element in manufacturers:
        try:
            dict_[element] = dict_[element] + 1
        except KeyError:
            dict_[element] = 1
    return dict_


def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """

    total_games = 0
    games_count = 0
    for element in table:
        if element[game_manufacturer] == manufacturer:
            total_games = total_games + int(element[game_count])
            games_count += 1
    return(total_games/games_count)
