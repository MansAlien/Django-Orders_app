FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["sh", "./start.sh"]