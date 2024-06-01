FROM python:3.9-slim

WORKDIR /app

COPY services/restock/restock_service.py /app/

RUN pip install flask

CMD ["python", "restock_service.py"]

