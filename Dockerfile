FROM python:3

RUN pip install boto3 

COPY main.py /

COPY infrastructure_builder.py /

COPY .env /

CMD [ "python", "./main.py" ]