#-*- coding: utf-8 -*-

import requests
import pandas as pd


def webDataToCsv1(url, csv_name):
    df = webDataToDF1(url)
    df.to_csv(csv_name)
    return df


def test1():
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
