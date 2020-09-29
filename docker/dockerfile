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

