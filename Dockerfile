FROM python:3.12.3

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

WORKDIR /app/blog_api

CMD ["flask", "--app","api", "run", "--port", "5100", "--host", "0.0.0.0"]