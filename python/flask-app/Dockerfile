FROM python:3.8-slim

WORKDIR /flask_app

COPY . /flask_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]