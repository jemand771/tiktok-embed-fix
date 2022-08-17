FROM python:3.10

WORKDIR /tmp
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn

WORKDIR /app
COPY *.py ./
COPY templates ./templates

EXPOSE 80

CMD ["gunicorn", "main:app", "--bind", ":80"]
