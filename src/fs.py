#!/usr/bin/python3

## Project: To fetch closing-price for NDAYS of a stock SYMBOL
## From Alphavantage API
## Author: Ven Para
## Date: 28-Sep-2020

from alpha_vantage.timeseries import TimeSeries
import pandas
import sys
import time
#import matplotlib.pyplot as plt

## python function to fetch the closing-price for NDAYS of a SYMBOL
## And write to a webpage called templates/test.html

def Fetchstock(APIKEY: str, SYMBOL: str, NDAYS: int):
	ts = TimeSeries(key=APIKEY, output_format='pandas')
	data, meta_data = ts.get_daily_adjusted(symbol=SYMBOL, outputsize='compact');

	stockfile = open("templates/test.html", "w")
	html1 = "<html>\n"
	html2 = "</html>\n"
	newline = "\n"
	para1 = "<pre>\n"
	para2 = "</pre>\n"
	stockfile.write(html1)
	stockfile.write("Stock Name: ")
	stockfile.write(SYMBOL)
	stockfile.write(newline)
	stockfile.write(para1)
	stockfile.write(str(data['4. close'][:NDAYS]))
	stockfile.write(newline)
	stockfile.write(para2)
	stockfile.write(newline)
	stockfile.write("Average Closing price: ")
	stockfile.write(str(data['4. close'][:NDAYS].mean()))
	stockfile.write(newline)
	stockfile.write(html2)
	stockfile.close()
