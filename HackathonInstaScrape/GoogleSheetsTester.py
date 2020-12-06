"""
Created on 12/5/2020

@author: sophie
"""

from openpyxl import Workbook

workbook = Workbook()
sheet = workbook.active

sheet["A1"] = "hello"
sheet["B1"] = "world!"

workbook.save(filename="hello_world.xlsx")

if __name__ == '__main__':
    pass