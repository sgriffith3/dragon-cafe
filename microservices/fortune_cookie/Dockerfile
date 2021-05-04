FROM python:3.8-slim
COPY requirements.txt /home/ubuntu/requirements.txt
RUN pip3 install -r /home/ubuntu/requirements.txt
COPY fortune_cookie.py /home/ubuntu/fortune_cookie.py  
COPY templates /home/ubuntu/templates
WORKDIR /home/ubuntu/
CMD ["python3", "/home/ubuntu/fortune_cookie.py"]
EXPOSE 2229
