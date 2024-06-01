FROM python:3.9-slim

WORKDIR /app

COPY services/consume/consume_service.py /app/

RUN pip install flask

CMD ["python", "consume_service.py"]
