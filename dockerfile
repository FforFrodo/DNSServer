FROM python:3-alpine

COPY . /app
WORKDIR /app

EXPOSE 53

CMD ["python", "simple_proxy.py"]
