FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg gcc g++ libffi-dev

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["hypercorn", "main:app", "--bind", "::"]
