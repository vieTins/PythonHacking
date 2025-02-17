print(b"hello")
print(b"hello".hex())

print(b"\x68\x65\x6c\x6c\x6f")
print(b"\x68\x65\x6c\x6c\x6f".hex())

de = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d" 
for i in range(0 , len(de) , 2 )  :
    print(chr(int(de[i:i+2] , 16)) , end = "")   

# lặp qua 2 ký tự một lần từ 0 đến len(de) , mỗi lần lấy 2 ký tự - bởi vì mỗi ký tự hexa cần 2 ký tự
# chuyển 2 ký tự hexa thành số nguyên và chuyển số nguyên thành ký tự   


print()
import base64 
print(bytes.fromhex("72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"))
print(base64.b64encode(bytes.fromhex("72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"))) # chuyển hex thành base64 

text = "HELLO"
print(text.encode().hex()) # chuyển text thành hex
print(int(text.encode().hex() , 16)) # chuyển hex thành số nguyên

number = "11515195063862318899931685488813747395775516287289682636499965282714637259206269"
print(bytes.fromhex(hex(int(number))[2:])) # chuyển số nguyên thành hex và chuyển hex thành text