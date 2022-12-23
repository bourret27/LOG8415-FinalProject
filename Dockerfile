FROM python:3

RUN pip install boto3 

COPY main.py /

COPY infrastructure_builder.py /

COPY .env /

COPY setup_scripts/standalone.sh /

COPY setup_scripts/master.sh /

COPY setup_scripts/slave.sh /

ENTRYPOINT [ "python", "./main.py" ]