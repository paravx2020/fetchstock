# fetchstock
Fetch and Show the stock price for a SYMBOL from Alpha-vantage
(Using Python, Docker and Kubernetes)

## Index

1. Python application using Flask
2. Creating & Testing a Docker Image
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

Run the above app with command line arguments as shown below 

**$ cd src/**

**$ python main.py ReplaceWithYourAPIKEY MSFT 7**
```
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

And when you copy the link below and run in browser, you can see the output webpage (templates/test.html) as shown below.
http://0.0.0.0:5000/

## Creating & Testing a Docker image:

Below is the 'dockerfile' code:
**$ cat dockerfile**
``` 
FROM python:3.7

ENV APIKEY="replaceMe"
ENV SYMBOL="MSFT"
ENV NDAYS=7

# Create app directory
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 5000
ENTRYPOINT [ "python", "/app/main.py" ]
CMD [ "$APIKEY, "$SYMBOL", "$NDAYS" ] 

```
Now we need to create the Docker image. If you are using the 'minikube', make sure you run the command below so that the docker will be created on that node.

step1: Start minikube
```
$ minikube start
😄  minikube v1.13.1 on Ubuntu 18.04
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.19.2 on Docker 19.03.8 ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" by default
```
Step2: Run the command below
```
$ eval $(minikube docker-env)

$ docker image ls
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
hello-python                              latest              460492c64502        41 hours ago        885MB
k8s.gcr.io/kube-proxy                     v1.19.2             d373dd5a8593        12 days ago         118MB
k8s.gcr.io/kube-controller-manager        v1.19.2             8603821e1a7a        12 days ago         111MB
k8s.gcr.io/kube-apiserver                 v1.19.2             607331163122        12 days ago         119MB
k8s.gcr.io/kube-scheduler                 v1.19.2             2f32d66b884f        12 days ago         45.7MB
python                                    3.7                 11c6e5fd966a        2 weeks ago         876MB
gcr.io/k8s-minikube/storage-provisioner   v3                  bad58561c4be        3 weeks ago         29.7MB
k8s.gcr.io/etcd                           3.4.13-0            0369cf4303ff        4 weeks ago         253MB
kubernetesui/dashboard                    v2.0.3              503bc4b7440b        3 months ago        225MB
k8s.gcr.io/coredns                        1.7.0               bfe3a36ebd25        3 months ago        45.2MB
kubernetesui/metrics-scraper              v1.0.4              86262685d9ab        6 months ago        36.9MB
k8s.gcr.io/pause                          3.2                 80d28bedfe5d        7 months ago        683kB
```

Step3: Create the docker image
```
$ docker build -t fetchstock .
Sending build context to Docker daemon  20.48kB
Step 1/11 : FROM python:3.7
 ---> 11c6e5fd966a
Step 2/11 : ENV APIKEY="replaceMe"
 ---> Using cache
 ---> f990ee4ab5fb
Step 3/11 : ENV SYMBOL="MSFT"
 ---> Using cache
 ---> fe1f73ef5adc
Step 4/11 : ENV NDAYS=7
 ---> Using cache
 ---> d3da6ac1daef
Step 5/11 : WORKDIR /app
 ---> Using cache
 ---> d292da795558
Step 6/11 : COPY src/requirements.txt ./
 ---> Using cache
 ---> 36bdb4dbcafb
Step 7/11 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> a832a838b6b2
Step 8/11 : COPY src /app
 ---> 7d998ce2bcfb
Step 9/11 : EXPOSE 5000
 ---> Running in fe6bec512809
Removing intermediate container fe6bec512809
 ---> 917ffe040861
Step 10/11 : ENTRYPOINT [ "python", "/app/main.py" ]
 ---> Running in 69a804d48342
Removing intermediate container 69a804d48342
 ---> 6f4052c60001
Step 11/11 : CMD [ "$APIKEY, "$SYMBOL", "$NDAYS" ]
 ---> Running in 116295fd578b
Removing intermediate container 116295fd578b
 ---> e7394010c3fc
Successfully built e7394010c3fc
Successfully tagged fetchstock:latest

```
Make sure the image is now created 
```
$ docker image ls |grep fetchstock
fetchstock                                latest              e7394010c3fc        About a minute ago   1.03GB
```
## Kubernetes manifests and testing on 'minikube'

Step1: Enable tunnel on minikube so that our app can be accessible on web

Run this command in a seperate terminal (this is something similar to kubectl port-forwarding)

**$ minikube tunnel**
```
[sudo] password for ubuntu: 
Status:	
	machine: minikube
	pid: 14257
	route: 10.96.0.0/12 -> 172.17.0.2
	minikube: Running
	services: []
    errors: 
		minikube: no errors
		router: no errors
		loadbalancer emulator: no errors
```
Step2: Apply kubernetes manifest(s) to create namespace(fetchstock), deployment, service, secret (for APIKEY) and configmap (for SYMBOL & NDAYS)

**$ cd k8s/**
```
$ kubectl apply -f fs-deploy.yaml 
namespace/fetchstock created
configmap/fetchstock-config created
secret/apikey-secret created
service/fetchstock-service created
deployment.apps/fetchstock created

$ kubectl get deployments -n fetchstock
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
fetchstock   2/2     2            2           28s

$ kubectl get pods -n fetchstock
NAME                          READY   STATUS    RESTARTS   AGE
fetchstock-558644d697-c74fr   1/1     Running   0          36s
fetchstock-558644d697-j7xg7   1/1     Running   0          36s

$ kubectl get svc -n fetchstock
NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
fetchstock-service   LoadBalancer   10.108.238.187   10.108.238.187   8000:30573/TCP   42s
```
## Output:
Based on the IP address (when you run), you can access the stock closing-price over N days and its average.
As you can see in the 'fetchstock-service' above, the app is now exposed on http://{EXTERNAL-IP}:8000

You can also check this in ![test.html](src/templates/test.html)

## Delete the K8s resources
Once tested successfully, you can delete the resources as shown below
```
$ kubectl delete -f fs-deploy.yaml 
namespace "fetchstock" deleted
configmap "fetchstock-config" deleted
secret "apikey-secret" deleted
service "fetchstock-service" deleted
deployment.apps "fetchstock" deleted

$ kubectl get deployments -n fetchstock
No resources found in fetchstock namespace.

$ kubectl get pods -n fetchstock
No resources found in fetchstock namespace.

$ kubectl get svc -n fetchstock
No resources found in fetchstock namespace. 
```

