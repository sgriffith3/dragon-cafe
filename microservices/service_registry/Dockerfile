FROM python:3.8-slim
COPY service_registry.py .
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
CMD python3 service_registry.py
EXPOSE 55555