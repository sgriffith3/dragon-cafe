import os
import socket
import requests

LOCAL_IP = socket.gethostbyname(socket.gethostname())
LOCAL_PORT = os.getenv("DRAGON_PORT", 2224)
REG_ADDR = os.getenv("SR_ADDRESS", "127.0.0.1")
REG_PORT = os.getenv("SR_PORT", 55555)


def register(service):
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/add/{service}/{LOCAL_IP}/{LOCAL_PORT}")
    print(r.status_code)


def unregister(service):
    r = requests.get(f"http://{REG_ADDR}:{REG_PORT}/remove/{service}/{LOCAL_IP}/{LOCAL_PORT}")
    print(r.status_code)


register(os.path.basename(__file__).rstrip(".py"))
print("Added")

unregister(os.path.basename(__file__).rstrip(".py"))
print("Deleted")
