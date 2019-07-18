FROM python:3.7-slim

RUN pip3 install requests

ADD app.py /app.py

ENTRYPOINT ["python3", "/app.py"]