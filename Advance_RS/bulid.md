# Advanced Reverse Shell

Cập nhật thêm tính năng của RS cũ

**Về Server**

- Với các câu lệnh như `help , use , list , exit` thì sẽ in ra giải thích
- Hỗ trợ kết nối nhiều hơn , nghĩa là hacker có thể xử lý nhiều thiết bị từ một máy chủ trung tâm
- Chấp nhận kết nối từ client trên một luồng riêng biệt
- Gửi và nhận file từ client với các lệnh `download` , `upload`

**Vể Client**

- Chụp ảnh màn hình từ xa , dùng lệnh `screenshot` để yêu cầu client chụp ảnh màn hình hiện tại
- Ghi âm bằng microphone bằng lệnh `recordmic <time>` để yêu cầu client ghi âm trong time cụ thể
- Thu nhập thông tin hệ thống bằng lệnh `sysinfo` , thu nhập thông tin phần cứng và hệ điều hành
