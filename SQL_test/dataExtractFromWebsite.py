#-*- coding: utf-8 -*-

"""
sources:

https://stackoverflow.com/questions/11790535/extracting-data-from-html-table
https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python

http://www.python-excel.org/
https://stackoverflow.com/questions/16560289/using-python-write-an-excel-file-with-columns-copied-from-another-excel-file
https://stackoverflow.com/questions/19189048/writing-creating-a-worksheet-using-xlrd-and-xlwt-in-python

"""

import sys
import os
import requests
import pandas as pd
import xlrd
import xlwt
import pickle
import urllib
from bs4 import BeautifulSoup


def webDataTableToExcel(url, ExcelName):
    pass


def webDataToDict_table(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    webData_list = []
    for table in tables:
        last_title = None
        lines = table.find_all("tr")
        for line in lines:
            line_info = []
            if line.find("td", attrs={"colspan":"2"}) != None:
                last_title = line.find("td", attrs={"colspan":"2"}).text.strip()
            else:
                name = line.find("td", attrs={"class":"tdd"}).text.strip().split("\n")[0]
                info = line.find("td", attrs={"class":"tdd"}).text.strip().split("\n")[1]
                adress = info.split('ADRES :')[1].split('TELEFON :')[0]
                tel = info.split('ADRES :')[1].split('TELEFON :')[1].split('Fax: ')[0]
                fax = info.split('ADRES :')[1].split('TELEFON :')[1].split('Fax: ')[1]
                coordinate = str(line.find("td", attrs={"class":"noBackground"}).find("span"))
                coordinate = coordinate.split('onclick="goster')[1].split('" style=')[0]
                line_info.append(last_title)
                line_info.append(name)
                line_info.append(adress)
                line_info.append(tel)
                line_info.append(fax)
                line_info.append(coordinate)
                webData_list.append(line_info)

    return webData_list


def write_xlsx(wb_dict, path):
    """
    write a dict as wb_dict[sheet_name][row_index][col_index][cell_value] to a xlsx Excel file.
    """
    workbook = xlwt.Workbook()
    for sheet_name in wb_dict.keys():
        sheet = workbook.add_sheet(sheet_name)
        for row_index in range(len(wb_dict[sheet_name])):
            for col_index in range(len(wb_dict[sheet_name][row_index].keys())):
                sheet.write(row_index, col_index, wb_dict[sheet_name][row_index][col_index])
    workbook.save(path)


url1 = "http://www.igdas.istanbul/AdresVeTelefonlar?id=233&lang=tr&sc=4"
list = webDataToDict_table(url1)
for line in list:
    print line
    coordinate = ''.join(c for c in line[-1].split(",")[0] if c.isdigit())
    coordinate = coordinate + "." + ''.join(c for c in line[-1].split(",")[1] if c.isdigit())
    coordinate = coordinate + ", " + ''.join(c for c in line[-1].split(",")[2] if c.isdigit())
    coordinate = coordinate + "." + ''.join(c for c in line[-1].split(",")[3] if c.isdigit())
    #print line[0],"####", line[1],"####", line[-1], "####", coordinate

url2 = "http://www.igdas.istanbul/IgdasSubeleri?id=236&lang=tr&sc=4"


def webDataToCsv1(url, csv_name):
    df = webDataToDF1(url)
    df.to_csv(csv_name)
    return df


def test_webDataToCsv1():
    url1 = 'http://www.ffiec.gov/census/report.aspx?year=2011&state=01&report=demographic&msa=11500'
    csv_name1 = 'my data.csv'
    df1 = webDataToCsv1(url1, csv_name1)
    print df1


def webDataToDF1(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    return df


def dfToCsv(df, csv_name):
    pass



def test_webDataToDF1():
    url2 = 'http://www.igdas.istanbul/AdresVeTelefonlar?id=233&lang=tr&sc=4'
    csv_name2 = 'AdresVeTelefonlar.csv'
    df = webDataToDF1(url2)
    df.drop(1, axis=1, inplace=True)
    keys = []
    table_dict = {}
    last_key = None
    for line in df[0]:
        if len(line) < 40:
            last_key = line
            table_dict[line] = []
            keys.append(line)
        else:
            table_dict[last_key].append(line)

    resultTable_dict = {u"Bina Türü":{}, u"Başlık":{}, u"Adres":{}, u"Telefon":{}, u"Faks":{}}
    lastIndex = 0
    for key in keys:
        for index in range(len(table_dict[key])):
            row = lastIndex + index
            if index == (len(table_dict[key]) - 1):
                lastIndex = row


    for key in keys:
        print "##Bina Türü## ", key
        for lineIndex in range(len(table_dict[key])):
            print "##Başlık## ", table_dict[key][lineIndex].split("ADRES :")[0], "##Adres## ", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[0], "##TEL##", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[1].split("Fax: ")[0], "##Fax##", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[1].split("Fax: ")[1]


#test_webDataToDF1()
url2 = 'http://www.igdas.istanbul/IgdasSubeleri?id=236&lang=tr&sc=4'
df = webDataToDF1(url2)
#print df