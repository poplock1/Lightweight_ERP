""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common

title_list = ["ID", "Game title", "Price in USD", "Month", "Day", "Year"]
input_list = ["Game title", "Price in USD", "Month", "Day", "Year"]
filename = "sales/sales.csv"
game_id = 0
game_title = 1
game_price = 2
game_month = 3
game_day = 4
game_year = 5


def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.

    Returns:
        None
    """

    # your code
    table = data_manager.get_table_from_file(filename)
    while True:
        options = ["Show table",
                   "Add",
                   "Remove",
                   "Update",
                   "Get lowest price item",
                   "Items sold in given time range"]
        ui.print_menu("Sales Menagement menu", options, "Exit menu")
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
            ui.print_result(get_lowest_price_item_id(
                table), "Lowest price game index:\n")
        elif option == "6":
            correct_input = 0
            while correct_input == 0:
                month_from = ui.get_inputs(["Month from: "], "Provide data")
                month_from = int(''.join(str(e) for e in month_from))
                day_from = ui.get_inputs(["Day from: "], "Provide data")
                day_from = int(''.join(str(e) for e in day_from))
                year_from = ui.get_inputs(["Year from: "], "Provide data")
                year_from = int(''.join(str(e) for e in year_from))
                month_to = ui.get_inputs(["Month to: "], "Provide data")
                month_to = int(''.join(str(e) for e in month_to))
                day_to = ui.get_inputs(["Day to: "], "Provide data")
                day_to = int(''.join(str(e) for e in day_to))
                year_to = ui.get_inputs(["Year to: "], "Provide data")
                year_to = int(''.join(str(e) for e in year_to))
                if month_from and month_to in range(1, 13):
                    if day_from and day_to in range(1, 32):
                        if year_from and year_to in range(1990, 2021):
                            ui.print_table(get_items_sold_between(table, month_from, day_from, year_from, month_to,
                                                                  day_to, year_to), title_list)
                            correct_input += 1
                else:
                    ui.print_error_message(
                        "Provide correct data: months 1->12, days 1->31, years 1990->2020")
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

    # your code
    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table (list): table to add new record to

    Returns:
        list: Table with a new record
    """

    # your code
    while True:
        new_record = ui.get_inputs(
            input_list, "Please provide personal information:\n")
        new_record.insert(0, common.generate_random([]))
        if not new_record[game_price].isdigit():
            ui.print_error_message("Wrong value typed. Price must be a number")
        elif not new_record[game_month].isdigit() or not int(new_record[game_month]) in range(1, 13):
            ui.print_error_message("Wrong value typed. Months can be 1 -> 12")
        elif not new_record[game_day].isdigit() or not int(new_record[game_day]) in range(1, 32):
            ui.print_error_message("Wrong value typed. Days can be 1 -> 31")
        elif not new_record[game_year].isdigit() or not int(new_record[game_year]) in range(1990, 2021):
            ui.print_error_message(
                "Wrong value typed. Year must be higher than 1990 and lower than 2020")
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

    # your code
    for element in table:
        if element[game_id] == id_:
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

    # your code
    index = common.get_ind(table, game_id, id_)
    for element in table:
        if element[game_id] == id_:
            while True:
                new_record = ui.get_inputs(
                    input_list, "Please provide personal information:\n")
                new_record.insert(0, common.generate_random([]))
                if not new_record[game_price].isdigit():
                    ui.print_error_message(
                        "Wrong value typed. Price must be a number")
                elif not new_record[game_month].isdigit() or not int(new_record[game_month]) in range(1, 13):
                    ui.print_error_message(
                        "Wrong value typed. Months can be 1 -> 12")
                elif not new_record[game_day].isdigit() or not int(new_record[game_day]) in range(1, 32):
                    ui.print_error_message(
                        "Wrong value typed. Days can be 1 -> 31")
                elif not new_record[game_year].isdigit() or not int(new_record[game_year]) in range(1990, 2021):
                    ui.print_error_message(
                        "Wrong value typed. Year must be higher than 1990 and lower than 2020")
                else:
                    table[index] = new_record
                    break
    return table


# special functions:
# ------------------

def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title

    Args:
        table (list): data table to work on

    Returns:
         string: id
    """

    # your code
    lowest_price = max(game[game_price] for game in table)
    for game in table:
        if game[game_price] < lowest_price:
            lowest_price = game[game_price]
            lowest_price_id = game[game_id]
    return lowest_price_id


def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)

    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)

    Returns:
        list: list of lists (the filtered table)
    """

    # your code
    games_in_years = []
    games_in_range = []
    for game in table:
        if year_from <= int(game[game_year]) and year_to >= int(game[game_year]):
            games_in_years = games_in_years + [game]
    for game in games_in_years:
        if int(game[game_year]) == year_from:
            if month_from < int(game[game_month]):
                games_in_range.append(game)
            elif month_from == int(game[game_month]):
                if day_from <= int(game[game_day]):
                    games_in_range.append(game)
        if int(game[game_year]) == year_to:
            if month_to > int(game[game_month]):
                games_in_range.append(game)
            elif month_to == int(game[game_month]):
                if day_to >= int(game[game_day]):
                    games_in_range.append(game)
    return games_in_range
