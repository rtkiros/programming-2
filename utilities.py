from pathlib import Path
import re


def get_project_root_dir():
    """
    Method to get the root dir of the project
    :return:
    """
    path = Path(__file__).parent
    return path


def get_clean_number_list(number_list):
    """
    Method to clean a the list with the numbers of the CCS classification from the report file
    THe report are not always correct interpreted, so this method clean the list with information
    :param number_list: list which must be cleaned
    :return: list with the cleaned numbers
    """
    new_numbers = []
    for item in number_list:
        if item == "":
            pass
        elif item == "-":
            new_numbers.append(0)
        elif item.isnumeric():
            new_numbers.append(int(item))
        elif item == "B":
            new_numbers.append(13)
        else:
            only_numbers = re.split("[^0-9]", item)
            only_numbers = get_clean_number_list(only_numbers)
            new_numbers = [*new_numbers, *only_numbers]

    return new_numbers
