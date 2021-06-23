FROM python:3.8-slim
COPY requirements.txt /home/ubuntu/requirements.txt
RUN pip3 install -r /home/ubuntu/requirements.txt
COPY api_gateway.py /home/ubuntu/api_gateway.py  
COPY templates /home/ubuntu/templates
WORKDIR /home/ubuntu/
CMD ["python3", "/home/ubuntu/api_gateway.py"]
EXPOSE 80
