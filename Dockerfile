FROM python:3.9.7-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc python3-dev default-libmysqlclient-dev &&\
    apt-get clean

WORKDIR /backend

COPY ./requirements.txt /backend/

RUN pip install -r requirements.txt

COPY ./ /backend/

# Expose the port (assuming your React app runs on port 3000)
EXPOSE 80

CMD ["python", "app.py"]

# CMD ["flask", "run", "--host=0.0.0.0"]