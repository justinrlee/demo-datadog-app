FROM python:3.7-alpine

RUN pip3 install requests

ADD app.py /

# RUN chmod +x
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/usr/local/bin/python3", "/app.py"]