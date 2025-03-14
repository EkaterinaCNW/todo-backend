FROM python:3.9-slim as todolist

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 8000
CMD ["gunicorn", "web_server:app", "-b :8000"]