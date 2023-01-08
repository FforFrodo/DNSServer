FROM python:alpine

COPY . /app
WORKDIR /app

EXPOSE 53

CMD ["python", "simple_proxy.py"]
