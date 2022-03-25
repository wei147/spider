# https://music.163.com/weapi/comment/resource/comments/get?csrf_token=6b98516f7cbf6206113b366d7b727cb5 登录后会有token
# https://music.163.com/weapi/comment/resource/comments/get?csrf_token=

# 1.找到未加密的参数
# 2.想办法把参数进行加密（必须参考网易的逻辑），params => encText, encSecKey => encSecKey
# 3.请求到网易,拿到评论数据

# 需要安装pycrypto      pip install pycrypto
from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
# 请求方式是POST

data = {"csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        # "rid": "R_SO_4_1325905146",
        # "threadId": "R_SO_4_1325905146",
        "rid": "R_SO_4_1345353903",
        "threadId": "R_SO_4_1345353903",
        }

# 服务于d的
f = "'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17" \
    "a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c" \
    "9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7' "
g = "0CoJUm6Qyw8W8jud"
e = "010001"
i = "Xx5NtaWg1hWGpJj7"  # 2022年3月21日18:51:38已更  手动固定的.  -> 人家函数中是固定,c()函数的结果就是固定的


def get_enSecKey():
    return "250aa942053ddf42b95a99517caed4c4de83c436a4c6e1dddab8398420e878572445eb505507c36ac97a20e90f00dbb0d32ae2db565c9e7524f7f95c0d9594acfbcb2e3997691bf01c33c5f221a3b7ab6db19d7cac7f83dee90e8055fbab37d12ced494977eb9408310547a6abb28a4ef31d3f7b914b83e7cc454d47ab37d134 "


# 把参数进行加密
def get_params(data):  # 默认这里接收到的是字符串
    first = enc_params(data, g)
    secend = enc_params(first, i)
    return secend  # 返回的就是params


# 转化成16的倍数，为下方加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


# 加密过程
def enc_params(data, key):  # 加密过程
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密, 加密的内容的长度必须是16的倍数
    b64encode(bs)
    return str(b64encode(bs), "utf-8")  # 转化成字符串返回


# 处理加密过程
"""
 function a(a=16) {     # 产生随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)      # 循环16次
            e = Math.random() * b.length,       #随机数 1.2345
            e = Math.floor(e),  # 取整    1
            c += b.charAt(e);   # 取字符串中的XXX位置   b
        return c
    }
    function b(a, b) {  # a是要加密的内容
        var c = CryptoJS.enc.Utf8.parse(b)  # b是秘钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)  # e是数据
          , f = CryptoJS.AES.encrypt(e, c, {    # c 加密的秘钥
            iv: d,  # 偏移量
            mode: CryptoJS.mode.CBC # 加密模式：cbc
        });
        return f.toString()
    }
    function c(a, b, c) {       # c里面不产生随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {            d:数据,  e:010001,  f:较长的字符串,     g:'0CoJUm6Qyw8W8jud'
        var h = {}      # 空对象
          , i = a(16);  # i就是一个16位的随机值, 把i设置成定值
        h.encText = b(d, g),    # g是秘钥
        h.encText = b(h.encText, i),    # 返回的就是params   i也是秘钥
        h.encSecKey = c(i, e, f),       # 得到的就是encSecKey, e和f是定死的, 如果此时把i固定,得到的key一定是固定的
        return h
    }
    
    两次加密:
    数据+g => b => 第一次加密+i => b =params
"""

# 'window.asrsea(JSON.stringify(i3x), bsR4V(["流泪", "强"]), bsR4V(Xp1x.md), bsR4V(["爱心", "女孩", "惊恐", "大笑"]));'

# 发送请求，得到评论结果
resp = requests.post(url, data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_enSecKey()
})
print(resp.text)
