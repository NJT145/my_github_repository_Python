#-*- coding: utf-8 -*-

import requests
import pandas as pd

def webDataToCsv1(url, csv_name):
    df = webDataToDF(url)
    df.to_csv(csv_name)
    return df


def test1():
    url1 = 'http://www.ffiec.gov/census/report.aspx?year=2011&state=01&report=demographic&msa=11500'
    csv_name1 = 'my data.csv'
    df1 = webDataToCsv1(url1, csv_name1)
    print df1

def webDataToDF(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    return df


def dfToCsv(df, csv_name):
    pass

url2 = 'http://www.igdas.istanbul/AdresVeTelefonlar?id=233&lang=tr&sc=4'
csv_name2 = 'AdresVeTelefonlar.csv'
df = webDataToDF(url2)
df.drop(1, axis=1, inplace=True)
print df
