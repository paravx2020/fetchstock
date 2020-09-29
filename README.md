# fetchstock
Fetch and Show the stock price for a SYMBOL from Alpha-vantage
(Using Python, Docker and Kubernetes)

## Index

1. Python application using Flask
    - Explanation
    - Testing
2. Creating a Docker Image
    - Explanation
    - Testing the Docker Image
3. Kuberentes manifests
    - ConfigMap for SYMBOL and NDAYS
    - Secret for APIKEY
    - Deployment 
    - Service
4. Testing the 'fetchstock' app on Minikube

## The Project files

Here is the list of files in this project:

```
.
├── docker
│   └── dockerfile
├── dockerfile
├── k8s
│   └── fs-deploy.yaml
├── README.md
└── src
    ├── fs.py
    ├── main.py
    ├── requirements.txt
    └── templates
        └── test.html
```

## Python application with Flask

The following is a Python function to fetch the stock closing price for N days from Alphavantage API.
You need a API key from Alphavantage which you can generate free from their website. The collected stock data is written to a HTML file called templates/html.test
The INPUTS required for this function are: APIKEY, SYMBOL and NDAYS


```
$ cat fs.py

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
```
Now, take a look at the Flask app which makes use of the above function.
It is using command-line arguments for getting the values for APIKEY, SYMBOL and NDAYS as shown below.

```
$ cat src/main.py

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

```
