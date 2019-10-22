#`!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a class for a house listing

The listing class contains functionality to get all info for a listing"""

import re
from enum import Enum
from .google_maps import GMaps

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class Utility:
    """Utility class that contains a Utility"""

    def __init__(self, possible_strs, cost):
        self.possible_strs = possible_strs
        self.cost = cost


class Utilities(Enum):
    """Enum for all utilities"""

    INTERNET = Utility(["High-Speed Internet"], 45)
    HEAT = Utility(["Heat"], 1400 / 12)  # Winter heat cost / 12 mo
    LAUNDRY = Utility({"Laundry Access",
                       "Washer/Dryer in Unit",
                       "Laundry Room"}, 50)  # laundromatt cost + hassle
    ELECTRIC = Utility(["Electricity"], .1724 * 750)  # Cost per kwhr * avg kwhr
    WATER = Utility(["Water"], 25)


class Pets(Enum):
    CONSIDERED = "Considered"
    ALL = "Pets Allowed"
    CATS = "Pets Allowed (Cats)"
    DOGS = "Pets Allowed (Dogs)"
    NOT_ALLOWED = "Pets Not Allowed"


class Listing:
    """House listing class that contains all info on a listing"""

    def __init__(self, soup, base_url, logger):
        """Stores the soup and the url"""

        self.soup = soup
        # Can't use the actual url here because it adds search query parameters
        # (It gets ugly)
        self.url = base_url + self.soup.findAll("a")[0].get("href")
        self.logger = logger

    def __repr__(self):
        """Returns a formatted string for all attributes we care about"""

        return "\n".join(["{}: {}".format(x, getattr(self, x))
                          for x in Listing.header_info()]) + "\n"

    def __lt__(self, other):
        """Comparison operator for sorting houses"""

        self.total_cost < other.total_cost

    def calculate_all(self, specific_soup, wage=42, max_roomates=1):
        """Calculates all the attributes we care about.

        Note: self.specific soup needs to be set before this func is called"""

        self.specific_soup = specific_soup
        self._get_price()
        self._get_address()
        self._get_commute_info(wage)
        # Needs specific soup to be able to run the funcs below
        self._get_beds()
        self._get_utilities_pets_included()
        self._get_total_cost(max_roomates)

    @property
    def row(self):
        """Returns a row for the csv of this listing"""

        return [getattr(self, x) for x in Listing.header_info()]

    @staticmethod
    def header_info():
        """Gets header information for the csv of this listing"""

        return ["price",
                "drive_time",
                "walk_time",
                "total_cost",
                "address",
                "url",
                "utils_cost",
                "drive_cost",
                "walk_cost"]

########################
### Helper Functions ###
########################

    def _get_price(self):
        """Sets price"""

        try:
            # Gets price string and removes commas from 1,000
            price_str = str(self.soup.findAll("div",
                            {"class": "price"})[0].text).replace(",", "")
            self.price = re.findall(r'\d+', price_str)[0]
        except:
            # If the price cannot be found, discard by setting price high
            self.price = 100000

    def _get_address(self):
        """Gets address and remove spaces"""

        self.address = str(self.soup.findAll("span", {"class": "address"}
                                             )[0].string).lstrip()

    def _get_commute_info(self, wage):
        """Gets drive and walking commute info"""

        self.logger.info("Calculating commute time for {}".format(self.url))
        # Consider parallelizing this for faster throughput?
        self.drive_time, self.walk_time = GMaps(
            self.logger).calculate(self.address)
        self._get_walk_price(wage)
        self._get_drive_price(wage)

    def _get_walk_price(self, wage):
        """Gets walk price based on time spent walking"""

        # Multiply by 2 for round trip, divide by 60 for per hour, * wage
        self.walk_cost = int(self.walk_time)*2/60 * wage

    def _get_drive_price(self,
                         wage,
                         mpg=21,
                         gas_cost_per_gallon=3,
                         mph=35,
                         parking_pass_price_per_year=240):
        """Gets drive price based on a variety of factors"""

        # We multiply by 2 to get both ways, /60 for per hour
        drive_time_per_hour = int(self.drive_time)*2/60
        # Gets drive time cost
        drive_time_cost = drive_time_per_hour*wage

        # Multiplies the miles by cost per mile (gas)
        gas_cost = drive_time_per_hour / mph * gas_cost_per_gallon * mpg

        # Cost of a parking pass per month (per month cause everythings per mo)
        parking_pass_cost = parking_pass_price_per_year/12

        self.drive_cost = drive_time_cost + gas_cost + parking_pass_cost

########################################
### Funcs that require specific_soup ###
########################################

    def _get_beds(self):
        try:
            # Gets bed numbers
            soup = list(self.specific_soup.find_all("p",
                                                    {"class": "bedbath"}))[0]
            beds_str = " ".join(soup.stripped_strings)
            # Gets digits
            digits = [int(s) for s in beds_str.split("bed")[0] if s.isdigit()]
            # Finds kind of home
            soup = list(self.specific_soup.find_all("span",
                                                    {"class": "unit"}))[0]
            if "per bedroom" not in " ".join(soup.stripped_strings):
                self.beds = digits[0]
            else:
                self.beds = 1
        except:
            # If the above fails, assume it has one bedroom
            self.beds = 1

    def _get_utilities_pets_included(self):
        utils_str = " ".join(list(self.specific_soup.find_all("ul",
            {"class": "snapshot-extras-list"}))[0].stripped_strings)

        self.included_utils = set()

        for utility in Utilities.__members__.values():
            for possible_str in utility.value.possible_strs:
                if possible_str in utils_str:
                    self.included_utils.add(utility.value)

        self.utils_cost = sum([util.cost for util in self.included_utils])

        for pet_option in Pets.__members__.values():
            if pet_option.value in utils_str:
                self.pets = pet_option.value

    def _get_total_cost(self, max_roomates):
        """Gets total_cost of listing"""

        # Divide total cost by number of expected roomates
        beds = self.beds if self.beds < max_roomates else max_roomates

        self.total_cost = min(self.walk_cost, self.drive_cost)
        self.total_cost += (int(self.price) + self.utils_cost) / beds
