FROM python:3.8

RUN mkdir -p ../src/test
WORKDIR ../src/test

COPY /bar/core/test ../src/test

CMD ['python3', 'test.py']
