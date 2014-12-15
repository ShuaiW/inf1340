#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = "Shuai Wang"
__email__ = "info.shuai@gmail.com"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases
        to decide
    :param watchlist_file: The name of a JSON formatted file that contains
        names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept",
        "Reject", "Secondary", and "Quarantine"
    """
    # parse three json files into lists
    input_content = parse_json(input_file)
    watchlist_content = parse_json(watchlist_file)
    first_name, last_name, passport = divide_watchlist(watchlist_content)
    countries_content = parse_json(countries_file)

    # medical advisory countries (lower case country code)
    ma_countries = [c.lower() for c in countries_content
                    if countries_content[c]["medical_advisory"] != ""]

    # visitor visa countries (lower case country code)
    visitor_countries = [c.lower() for c in countries_content
                         if countries_content[c]["visitor_visa_required"]
                         == "1"]

    # transit visa countries (lower case country code)
    transit_countries = [c.lower() for c in countries_content
                         if countries_content[c]["transit_visa_required"]
                         == "1"]

    input_length = len(input_content)

    # default "Accept" unless "Quarantine", "Reject", or "Secondary"
    output = [["Accept"] for i in range(input_length)]

    # iterate through the entry lists
    for idx in range(input_length):

        # 1. "Quarantine": a traveler comes from OR via a country that has
        # a medical advisory
        if ("from" in input_content[idx] and
            input_content[idx]["from"]["country"].lower() in ma_countries) or\
            ("via" in input_content[idx] and input_content[idx]["via"]
           ["country"].lower() in ma_countries):
                output[idx].append("Quarantine")

        # 2. "Reject": incomplete info, invalid passport, or invalid date
        if (not complete_info(input_content[idx])) or\
            (not valid_passport_format(input_content[idx]["passport"])) or\
            (not valid_date_format(input_content[idx]["birth_date"])) or\
            ("visa" in input_content[idx] and not
             valid_date_format(input_content[idx]["visa"]["date"])):
                output[idx].append("Reject")

        # "Reject": visit and from a country that needs visitor visa,
        # no visa or the visa is invalid
        if "entry_reason" in input_content[idx] and\
            input_content[idx]["entry_reason"].lower() == "visit" and\
           input_content[idx]["from"]["country"].lower() in visitor_countries:
                if "visa" not in input_content[idx]:
                    output[idx].append("Reject")
                else:
                    if not valid_visa(input_content[idx]["visa"]):
                        output[idx].append("Reject")

        # "Reject": transit and from a country that needs transit visa,
        # no visa or the visa invalid
        if "entry_reason" in input_content[idx] and\
            input_content[idx]["entry_reason"].lower() == "transit" and\
           input_content[idx]["from"]["country"].lower() in transit_countries:
                if "visa" not in input_content[idx]:
                    output[idx].append("Reject")
                else:
                    if not valid_visa(input_content[idx]["visa"]):
                        output[idx].append("Reject")

        # 3. "Secondary": name or passport on the watchlist
        if ("first_name" in input_content[idx] and
            input_content[idx]["first_name"].lower() in first_name and
            "last_name" in input_content[idx] and
            input_content[idx]["last_name"].lower() in last_name) or\
            ("passport" in input_content[idx] and
           input_content[idx]["passport"].lower() in passport):
                output[idx].append("Secondary")

    # make only one decision
    return distinct_decision(output)


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number
    characters separated by dashes

    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('^\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers

    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def parse_json(json_file):
    """
    Parses a json file into a list.

    :param json_file: json file
    :return: parsed list of the json file
    """
    try:
        with open(json_file, "r") as file_reader:
            file_contents = file_reader.read()
        return json.loads(file_contents)
    except FileNotFoundError:
        raise FileNotFoundError("File not found.")


def complete_info(entry):
    """
    Checks whether the entry is complete (containing all required info)

    :param entry: entry record of a traveler
    :return: Boolean True if the info is complete, False otherwise
    """
    required_info = ["first_name", "last_name", "from", "entry_reason",
                     "passport", "birth_date", "home"]
    if_complete = True

    for info in required_info:
        if info not in entry:
            if_complete = False
            break
    return if_complete


def divide_watchlist(watchlist):
    """
    Divide a watchlist into three sets: first_name, last_name and passport

    :param watchlist: a list containing watchlist content
    :return: three sets containing first_name, last_name and passport
    """
    first_name = set(entry["first_name"].lower() for entry in watchlist)
    last_name = set(entry["last_name"].lower() for entry in watchlist)
    passport = set(entry["passport"].lower() for entry in watchlist)
    return first_name, last_name, passport


def valid_visa(visa):
    """
    Checks whether a visa is valid

    :param visa: a traveler's visa info
    :return: Boolean True if visa is valid, False otherwise
    """
    if dates_difference(visa["date"]) < 730:
        return True
    return False


def dates_difference(date_string):
    """
    Calculates the difference in days of date given and current date

    :param date_string: date to be checked
    :return: the difference of two dates in days
    """
    if valid_date_format(date_string):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        current_date = datetime.date(year, month, day)

        visa_year, visa_month, visa_day = date_string.split("-")
        visa_date = datetime.date(int(visa_year), int(visa_month),
                                  int(visa_day))

        return (current_date - visa_date).days


def distinct_decision(decisions_list):
    """
    Outputs distinct immigration decision

    :param decisions_list: a list of entries contain one to four of the
        following strings: "Accept", "Reject", "Secondary", and "Quarantine"
    :return: a list of strings each represents the unique decision for that
        entry
    """
    output = []

    for entry in decisions_list:
        if "Quarantine" in entry:
            output.append("Quarantine")
        elif "Reject" in entry:
            output.append("Reject")
        elif "Secondary" in entry:
            output.append("Secondary")
        else:
            output.append("Accept")

    return output
