FROM python:2.7

COPY . /home/client

WORKDIR /home/client

RUN python setup.py install

CMD tail -f /dev/null
