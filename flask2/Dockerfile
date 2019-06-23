# Using Base image alpine with installed python3
FROM frolvlad/alpine-python3

MAINTAINER "Mayank Koli"

#choosing /usr/src/app as working directory
WORKDIR /usr/src/app

# Mentioned python module name to run application
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Exposing applicaiton on 5000 so that it can be accessible on default host(127.0.0.1) and port(5000).
EXPOSE 5000

#Copying code to working directory
COPY . .

#Making default entry as python will launch reverse.py
CMD [ "python3", "reverse.py" ]

