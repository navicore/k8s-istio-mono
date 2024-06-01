FROM python:3.9-slim

WORKDIR /app

COPY inventory_service.py /app/

RUN pip install flask

CMD ["python", "inventory_service.py"]

