FROM python:3.12-slim

WORKDIR /app

COPY markitdown /app/markitdown
COPY webapp/requirements.txt /app/webapp/requirements.txt
RUN pip install --no-cache-dir -r /app/webapp/requirements.txt \
    && pip install --no-cache-dir /app/markitdown

COPY webapp/main.py /app/webapp/main.py

EXPOSE 8080
CMD ["uvicorn", "webapp.main:app", "--host", "0.0.0.0", "--port", "8080"]
