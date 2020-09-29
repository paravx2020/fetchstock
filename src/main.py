## Project: To fetch closing-price for NDAYS of a stock SYMBOL
## From Alphavantage API
## Author: Ven Para
## Date: 28-Sep-2020

from fs import Fetchstock
from flask import Flask
from flask import render_template
import sys

### Command-line arguments 
APIKEY = str(sys.argv[1])
SYMBOL = str(sys.argv[2])
NDAYS = int(sys.argv[3])

app = Flask(__name__)

@app.route("/")
def fetch_stock():
    Fetchstock(APIKEY,SYMBOL,NDAYS)
    return render_template("test.html")
    
if __name__ == "__main__":
	app.run(host='0.0.0.0')
