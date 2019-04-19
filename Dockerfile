FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app
