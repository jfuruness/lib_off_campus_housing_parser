#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a class to create and save rows into excel"""

import xlsxwriter
from contextlib import contextmanager
from .listing import Listing


__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "MIT"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


@contextmanager
def open_excel(path):
    """context generator to open and close excel sheets"""

    spreadsheet = Spreadsheet(path)
    yield spreadsheet
    spreadsheet.close()


class Spreadsheet:
    """Creates and saves excel with rows"""

    def __init__(self, path="/tmp/off_campus.xlsx"):
        # Create workbook
        self.workbook = xlsxwriter.Workbook(path)
        # Add a worksheet
        self.worksheet = self.workbook.add_worksheet()
        # Starts off at row 0 and column 0
        self.row_num = self.col_num = 0
        # Write the header information
        self.write_rows([Listing.header_info()])

    def write_rows(self, rows):
        """Write rows to excel file"""

        for row_num, row_item in enumerate(rows):
            for col_num, cell_content in enumerate(row_item):
                self.worksheet.write(row_num + self.row_num,
                                     col_num + self.col_num, cell_content)
        # Save the last row
        self.row_num = self.row_num + row_num + 1

    def close(self):
        """Closes the workbook"""

        self.workbook.close()
