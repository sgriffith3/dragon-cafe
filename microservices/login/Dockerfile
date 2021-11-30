FROM python:3.8-slim
COPY requirements.txt /home/ubuntu/requirements.txt
RUN pip3 install -r /home/ubuntu/requirements.txt
COPY login.py /home/ubuntu/login.py  
COPY templates /home/ubuntu/templates
WORKDIR /home/ubuntu/
CMD ["python3", "/home/ubuntu/login.py"]
EXPOSE 2228
