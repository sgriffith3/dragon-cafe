FROM python:3.8-slim
COPY menu.py /home/ubuntu/menu.py  
COPY requirements.txt /home/ubuntu/requirements.txt
COPY templates /home/ubuntu/templates
RUN pip3 install -r /home/ubuntu/requirements.txt
WORKDIR /home/ubuntu/
CMD ["python3", "/home/ubuntu/menu.py"]
EXPOSE 2227
