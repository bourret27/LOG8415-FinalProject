FROM python:3

RUN pip install boto3

COPY main.py /

COPY .env /

CMD [ "python", "./main.py" ]