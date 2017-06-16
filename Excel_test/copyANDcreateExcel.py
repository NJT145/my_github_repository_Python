#-*- coding: utf-8 -*-

"""
sources:

http://www.python-excel.org/
https://stackoverflow.com/questions/16560289/using-python-write-an-excel-file-with-columns-copied-from-another-excel-file
https://stackoverflow.com/questions/19189048/writing-creating-a-worksheet-using-xlrd-and-xlwt-in-python

"""

import os
import requests
import pandas as pd
import xlrd
import xlwt
import pickle


def copy_sheet_xlsx(path, output_name):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)

    data = [sheet.cell_value(0, col) for col in range(sheet.ncols)]

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('test')

    for index, value in enumerate(data):
        sheet.write(0, index, value)

    workbook.save(output_name)


def read_xlsx(path):
    """
    that converts xlsx file to dict as wb_dict[sheet.name][row_index][col_index][cell_value] .
    """
    wb = xlrd.open_workbook(path)
    wb_dict = {}
    for sheet in wb.sheets():
        wb_dict.setdefault(sheet.name, {})
        for row_index in range(sheet.nrows):
            wb_dict[sheet.name].setdefault(row_index, {})
            for col_index in range(sheet.ncols):
                wb_dict[sheet.name][row_index].setdefault(col_index)
                wb_dict[sheet.name][row_index][col_index] = sheet.cell(row_index, col_index).value
    return wb_dict


def write_xlsx(wb_dict, path):
    """
    write a dict as wb_dict[sheet_name][row_index][col_index][cell_value] to a xlsx Excel file.
    """
    workbook = xlwt.Workbook()
    for sheet_name in wb_dict.keys():
        sheet = workbook.add_sheet(sheet_name)
        for row_index in range(len(wb_dict[sheet_name].keys())):
            for col_index in range(len(wb_dict[sheet_name][row_index].keys())):
                sheet.write(row_index, col_index, wb_dict[sheet_name][row_index][col_index])
    workbook.save(path)


pwd = os.getcwd()
print pwd
print ""
path_test_input = pwd+'\\test_input.xlsx'
print path_test_input
print ""
print read_xlsx(path_test_input)
print ""
#copy_sheet_xlsx(path_testCopy_input, 'testCopy_output.xls')
#print ""
path_testWrite = pwd+'\\testWrite.xls'
wb_dict = read_xlsx(path_test_input)
#write_xlsx(wb_dict, path_testWrite)
#print ""
