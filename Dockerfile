FROM python:3.10

ADD main.py .
ADD requirements.txt .
ADD bot_key.py .

RUN pip install -r ./requirements.txt

CMD ["python", "./main.py"]

