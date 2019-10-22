#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains an off campus parser

First you are logged in
Then all listings are found from general pages
Then all listings are found for specific listing pages
Then all listings are filtered
Then all listings are opened
You can filter listings manually
Once you hit enter all listings are saved in an excel doc"""

import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome as webstuff
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException
from .excel import open_excel
from .listing import Listing
from .logger import Logger


__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class Off_Campus_Parser:
    """Off Campus Parser that can parse all listings"""

    def __init__(self, executable_path='/home/anon/Downloads/chromedriver'):
        """Inits the browser and stores the url"""

        # Needs these environment vars to run properly
        self._check_for_environ_vars()
        self.browser = webstuff(executable_path=executable_path)
        self.url = "https://offcampushousing.uconn.edu"
        self.listings = []
        self.logger = Logger().logger

    def parse_houses(self,
                     drive_time_max=20,
                     max_rent=1500,
                     netid="jmf14015",
                     pets=False,
                     test=False,
                     excel_path="/tmp/off_campus.xlsx"):
        """Parses all houses.

        1. Logs into uconn off campus housing
        2. Parses all general pages with multiple listings
        3. Gets html for all specific listing pages
        4. Calculate all costs of each listing
        5. Open all listings
        6. Store relevant listings into a csv

        Filters by drive time max, and by pets if pets is True
        """

        self._login(self.url + "/login", max_rent, netid)

        # Parse all pages
        pages_left = True
        while pages_left:
            # Extends listings
            pages_left = self._parse_page()
            if test:
                break
        # Gets all listing info for the pages parsed
        self._get_listing_info()
        # Get rid of useless listings
        self._filter_listings(drive_time_max, pets)
        self._open_all_listings()
        input("After pressing enter all open pages will be saved into excel")
        with open_excel(excel_path) as spreadsheet:
            spreadsheet.write_rows(self.get_listing_rows())

    def _check_for_environ_vars(self):
        for key in ["google_api_key", "netid_password"]:
            if os.environ.get(key) in [None, ""]:
                raise Exception("Must input environment var: {}".format(key))

    def _login(self, login_url, max_rent, netid):
        """Logs user into uconn off campus housing"""

        self._load(login_url)
        # Find and click login
        login_box = self.browser.find_element_by_css_selector(
            ".login-block.sso-student")
        login_box.click()

        # Send netid keys and password keys and hit submit
        netid_box = self.browser.find_element_by_id("username")
        self._sleep(netid_box.send_keys(netid))
        pswd_box = self.browser.find_element_by_id("password")
        self._sleep(pswd_box.send_keys(os.environ.get("netid_password")))
        submit_box = self.browser.find_element_by_name("submit")
        self._sleep(submit_box.click())

        # Load the property search page and send max_rent
        self._load(self.url + "/property/search")
        max_rent_box = self.browser.find_element_by_id("rent-max")
        self._sleep(max_rent_box.send_keys(str(max_rent)), 5)

    def _sleep(self, func_call, sleep_time=.2):
        """Function gets wrapped with sleep"""

        time.sleep(sleep_time)
        return func_call

    def _load(self, page_url):
        """Loads a page and waits for ajax calls"""

        self._sleep(self.browser.get(page_url), 2)

    def _parse_page(self):
        """Parses the general page that has multiple listings, clicks next"""

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        # List comprehension of listings instances on the page
        self.listings.extend([Listing(x, self.url, self.logger) for x in
            soup.findAll("article", {"class": "compare_icon_init"})])
        # Returns False if cannot continue
        return self._click_next_page(soup)

    def _click_next_page(self, soup):
        """Clicks next page and return True, else return False"""

        try:
            next_box = self.browser.find_element_by_css_selector(
                ".next.load-more.scroll-up")
            self._sleep(next_box.click(), 3)
            return True
        except ElementNotVisibleException:
            return False
        except ElementNotInteractableException:
            return False

    def _get_listing_info(self, wage=45):
        """Calculates listing info"""

        for listing in self.listings:
            self._load(listing.url)
            listing.calculate_all(BeautifulSoup(self.browser.page_source,
                                                'html.parser'),
                                  wage)

    def _filter_listings(self, drive_time_max, pets):
        """Filters listings by drive time(int) and pets(bool)"""

        # If something is listed twice get rid of it
        unique_listings = list({x.url: x for x in self.listings}.values())
        # Filters by drive time and pets, then sorts by total_cost
        self.listings = sorted([x for x in unique_listings
                                if int(x.drive_time) <= drive_time_max
                                and (x.pets != "No" or not pets)])
        self.logger.info(self.listings)

    def _open_all_listings(self):
        """Opens all windows of listings"""

        for listing in self.listings:
            self.browser.execute_script("window.open('');")
            self._sleep(self.browser.switch_to_window(
                self.browser.window_handles[-1]))
            self._load(listing.url)

    def get_listing_rows(self):
        """Returns all listing rows that are open"""

        # Gets all URLs open
        urls = set()
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)
            urls.add(self.browser.current_url)

        # Return only listings that are open
        return [x.row for x in self.listings if x.url in urls]
