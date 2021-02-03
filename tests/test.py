# str = "abc||cb||hgf"
# print(str.split('||'))

from pyDes import *

# data = "Please encrypt my data"
# data = "1"
# k = des("DESCRYPT", CBC, "00000000", pad=None, padmode=PAD_PKCS5)
# d = k.encrypt(data)
# # print " %r" % d
# print('Encrypted:',d)
# # print "Decrypted: %r" % k.decrypt(d)
# print('Decrypted:',k.decrypt(d))
# # assert k.decrypt(d, padmode=PAD_PKCS5) == data
#
# from Crypto.Cipher import DES
import base64
# def encrypt_des(cipher):
#     if cipher is None:
#         return ""
#     try:
#         key = '1234A#CD'
#         # ECB方式
#         generator = DES.new(key, DES.MODE_ECB)
#         # 非8整数倍明文补位
#         pad = 8 - len(cipher) % 8
#         pad_str = ""
#         for i in range(pad):
#             pad_str = pad_str + chr(pad)
#         # 加密
#         encrypted = generator.encrypt(cipher + pad_str)
#         # 编码得密文
#         result = base64.b64encode(encrypted)
#         # print "cipher : "+str(cipher)+"  encrypted : "+result
#         return result
#     except Exception as e:
#         print(e)
#         return ""

def des_encrypt(s):
    secret_key = '1234A#CD'
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s.encode('utf-8'), padmode=PAD_PKCS5)
    return str(base64.b64encode(en), 'utf-8')

def des_descrypt(s):
    secret_key = '1234A#CD'
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(base64.b64decode(s), padmode=PAD_PKCS5)
    return de

data = '100000000000'
d = des_encrypt(data)
print('加密后：',d)
print('解密后：',des_descrypt(d))
