""" User Interface (UI) module """


def print_table(table, title_list):
    """
    Prints table with data.

    Example:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table (list): list of lists - table to display
        title_list (list): list containing table headers

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    # your goes code
    margin = 2
    correction = 1
    temp = ''
    for element in table:
        for e in element:
            if len(e) > len(temp):
                temp = e
    longest_word_table = len(temp)
    longest_word_title = len(max(title_list))

    column_width = max(longest_word_table, longest_word_title)+margin
    header = "/" + "-"*(column_width*len(title_list) +
                        len(title_list)-correction) + "\\"
    footer = "\\" + "-"*(column_width*len(title_list) +
                         len(title_list)-correction) + "/"
    row = ("|" + "-"*column_width)*len(title_list) + "|"

    print(header)
    for title in title_list:
        print("|" + title.center(column_width, ' '), end='')
    print("|")
    for rows in table:
        print(row)
        for element in rows:
            print("|" + element.center(column_width, ' '), end='')
        print("|")
    print(footer)


def print_result(result, label):
    """
    Displays results of the special functions.s

    Args:
        result: result of the special function (string, number, list or dict)
        label (str): label of the result

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print("\n" + label + "\n")
    if isinstance(result, list):
        for e in result:
            print(str(e) + ", ")
            print("\n")
        print("\n")
    elif isinstance(result, dict):
        for key, value in result.items():
            print(str(key) + " : " + str(value))
            print("\n")
        print("\n")
    elif result is int or float:
        print(str(result))
        print("\n")
    else:
        print(result)
        print("\n")


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        None: This function doesn't return anything it only prints to console.
    """
    print(title + ":\n")
    i = 1
    for e in list_options:
        print(f"\t ({i}) {e}")
        i += 1
    print(f"\t (0) {exit_message}")


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels (list): labels of inputs
        title (string): title of the "input section"

    Returns:
        list: List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    inputs = []
    print(title)
    for e in list_labels:
        inputs.append(input(str(e + ' ')))
        print("\n")
    return inputs


def print_error_message(message):
    """
    Displays an error message (example: ``Error: @message``)

    Args:
        message (str): error message to be displayed

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print(f"Error: {message}")
