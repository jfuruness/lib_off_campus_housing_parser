#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a class to create and save rows into excel"""

import googlemaps
from datetime import datetime
import os

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class GMaps:
    """Google maps class to find driving and walking distance"""

    def __init__(self, logger):
        """Creates Client with your google api key"""

        self.maps = googlemaps.Client(os.environ.get("google_api_key"))
        self.logger = logger

    def calculate(self, address, destination="UConn Bookstore"):
        """Calculates distance for walking and driving"""

        try:
            # Gets driving distance
            drive_result = self.maps.directions(address,
                                            destination,
                                            mode="driving",
                                            avoid="ferries",
                                            departure_time=datetime.now()
                                            )
            # Gets walking distance
            walk_result = self.maps.directions(address,
                                           destination,
                                           mode="walking",
                                           avoid="ferries",
                                           departure_time=datetime.now()
                                           )
        except googlemaps.exceptions.ApiError as e:
            self.logger.error(e)
            # If we cannot find it, return a very high number
            return 10000, 10000

        # Return the minutes for each rounded to the nearest whole number
        return (int(drive_result[0]['legs'][0]['duration']['value'])//60,
                int(walk_result[0]['legs'][0]['duration']['value'])//60)
